"""
Streamlit RAG Chatbot for Everstorm Outfitters Customer Support.

This application provides a chat interface for a RAG-based customer support
chatbot that answers questions using information from Everstorm documentation.
"""

import os
import logging
from typing import List, Tuple, Optional
from pathlib import Path

import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.llms import Ollama
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain.schema import Document
from pydantic import Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# Configuration Constants
# ============================================================================

# Embedding and model configuration
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "thenlper/gte-small")
LLM_MODEL: str = os.getenv("LLM_MODEL", "gemma3:1b")
LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.1"))

# Vector store configuration
FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH", "faiss_index")
RETRIEVAL_K: int = int(os.getenv("RETRIEVAL_K", "12"))

# UI configuration
MAX_DEBUG_CHUNKS: int = 5
MAX_CHUNK_PREVIEW_LENGTH: int = 400
SHOW_DEBUG_SECTION: bool = os.getenv("SHOW_DEBUG", "false").lower() == "true"

# Document filtering configuration
DEFAULT_EXCLUDE_KEYWORDS: List[str] = ["bigcommerce.com", "developer.bigcommerce.com"]

# System prompt template - improved for better synthesis
SYSTEM_TEMPLATE: str = """You are a helpful customer support chatbot for Everstorm Outfitters. Your job is to answer customer questions using ONLY the information provided in the context below.

IMPORTANT RULES:
1. Use ONLY the information from the CONTEXT section to answer the question.
2. If the answer is not clearly stated in the context, respond with: "I don't have that information in our documentation. Please contact our support team for assistance."
3. Synthesize the information into a clear, helpful answer. Do NOT just copy the raw text from the context.
4. Be concise, friendly, and professional.
5. If multiple relevant pieces of information are provided, combine them into a coherent answer.

CONTEXT FROM DOCUMENTS:
{context}

CUSTOMER QUESTION: {question}

YOUR ANSWER:"""


# ============================================================================
# Helper Functions
# ============================================================================

def extract_filename(source: str) -> str:
    """
    Extract filename from a file path.
    
    Args:
        source: File path string
        
    Returns:
        Filename extracted from path, or original string if no path separator found
    """
    return source.split('/')[-1] if '/' in source else source


def filter_documents(
    docs: List[Document], 
    exclude_keywords: Optional[List[str]] = None
) -> List[Document]:
    """
    Filter out documents from excluded sources (e.g., BigCommerce API docs).
    
    Args:
        docs: List of Document objects to filter
        exclude_keywords: List of keywords to exclude from sources. 
                         Defaults to DEFAULT_EXCLUDE_KEYWORDS.
    
    Returns:
        Filtered list of Document objects
    """
    if exclude_keywords is None:
        exclude_keywords = DEFAULT_EXCLUDE_KEYWORDS
    
    filtered = []
    for doc in docs:
        source = doc.metadata.get("source", "").lower()
        # Include Everstorm PDFs (from data/ folder)
        # Note: source is already lowercased, so no need for source.lower()
        if "data/everstorm" in source or ("everstorm" in source and ".pdf" in source):
            filtered.append(doc)
        # Exclude BigCommerce API documentation
        elif not any(keyword in source for keyword in exclude_keywords):
            # Include other documents that aren't BigCommerce API docs
            filtered.append(doc)
    return filtered


def validate_query(query: str) -> bool:
    """
    Validate that a user query is not empty.
    
    Args:
        query: User input query string
        
    Returns:
        True if query is valid (non-empty after stripping), False otherwise
    """
    return bool(query and query.strip())


# ============================================================================
# Custom Retriever Class
# ============================================================================

class FilteredRetriever(BaseRetriever):
    """
    Custom retriever that filters out BigCommerce API documentation.
    
    Wraps a base retriever and applies document filtering to exclude
    unwanted sources from retrieval results.
    """
    
    base_retriever: BaseRetriever = Field(..., description="The base retriever to wrap")
    
    class Config:
        arbitrary_types_allowed = True
    
    def _get_relevant_documents(self, query: str) -> List[Document]:
        """
        Retrieve documents and filter out excluded sources.
        
        Args:
            query: Search query string
            
        Returns:
            Filtered list of relevant Document objects
        """
        docs = self.base_retriever.get_relevant_documents(query)
        return filter_documents(docs)
    
    async def _aget_relevant_documents(self, query: str) -> List[Document]:
        """
        Async version of retrieval.
        
        Args:
            query: Search query string
            
        Returns:
            Filtered list of relevant Document objects
        """
        if hasattr(self.base_retriever, 'aget_relevant_documents'):
            docs = await self.base_retriever.aget_relevant_documents(query)
        else:
            docs = self.base_retriever.get_relevant_documents(query)
        return filter_documents(docs)


# ============================================================================
# Chain Loading Function
# ============================================================================

@st.cache_resource
def load_chain() -> Tuple[ConversationalRetrievalChain, FilteredRetriever]:
    """
    Load the FAISS vector store and create the RAG chain.
    
    Returns:
        Tuple of (chain, retriever) for the RAG pipeline
        
    Raises:
        FileNotFoundError: If FAISS index directory doesn't exist
        ValueError: If index cannot be loaded
    """
    try:
        # Validate index path exists
        index_path = Path(FAISS_INDEX_PATH)
        if not index_path.exists():
            raise FileNotFoundError(
                f"FAISS index directory not found: {FAISS_INDEX_PATH}. "
                "Please ensure the index has been built."
            )
        
        logger.info(f"Loading FAISS index from {FAISS_INDEX_PATH}")
        
        # Load embeddings
        embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
        
        # Load the saved vector store
        vectordb = FAISS.load_local(
            FAISS_INDEX_PATH, 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        
        # Create base retriever with higher k to account for filtering
        base_retriever = vectordb.as_retriever(search_kwargs={"k": RETRIEVAL_K})
        
        # Wrap with filtered retriever to exclude BigCommerce API docs
        retriever = FilteredRetriever(base_retriever=base_retriever)
        
        # Create prompt template
        prompt = PromptTemplate(
            template=SYSTEM_TEMPLATE, 
            input_variables=["context", "question"]
        )
        
        # Initialize LLM
        llm = Ollama(model=LLM_MODEL, temperature=LLM_TEMPERATURE)
        
        # Build the RAG chain
        chain = ConversationalRetrievalChain.from_llm(
            llm=llm, 
            retriever=retriever, 
            combine_docs_chain_kwargs={"prompt": prompt},
            return_source_documents=True,
            verbose=False
        )
        
        logger.info("RAG chain loaded successfully")
        return chain, retriever
        
    except FileNotFoundError:
        raise
    except Exception as e:
        logger.error(f"Error loading RAG chain: {e}")
        raise ValueError(f"Failed to load RAG chain: {str(e)}") from e


# ============================================================================
# Streamlit UI
# ============================================================================

def main() -> None:
    """Main Streamlit application function."""
    # Initialize chat history
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("chat_history", [])
    
    # Title
    st.title("🤖 Everstorm Customer Support Chatbot")
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # User input
    if prompt := st.chat_input("Ask a question about Everstorm..."):
        # Validate input
        prompt = prompt.strip()
        if not validate_query(prompt):
            st.warning("Please enter a question.")
            st.stop()
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get response from RAG chain
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Invoke the chain (it will retrieve documents internally)
                    result = chain.invoke({
                        "question": prompt, 
                        "chat_history": st.session_state.chat_history
                    })
                    response = result["answer"]
                    
                    # Show source documents (always useful for users)
                    if "source_documents" in result and len(result["source_documents"]) > 0:
                        with st.expander("📚 Sources used for this answer", expanded=False):
                            sources_used = set()
                            for doc in result["source_documents"]:
                                source = doc.metadata.get('source', 'Unknown')
                                filename = extract_filename(source)
                                sources_used.add(filename)
                            st.write("**Documents referenced:**")
                            for src in sorted(sources_used):
                                st.write(f"- {src}")
                    
                    # Optional debug section (only shown if SHOW_DEBUG=true)
                    if SHOW_DEBUG_SECTION and "source_documents" in result:
                        with st.expander("🔍 Debug: See retrieved chunk content", expanded=False):
                            retrieved_docs = result["source_documents"]
                            if len(retrieved_docs) == 0:
                                st.warning(
                                    "⚠️ No relevant documents found after filtering. "
                                    "The answer may not be accurate."
                                )
                            else:
                                st.write(f"**Found {len(retrieved_docs)} relevant chunks (after filtering):**")
                                for i, doc in enumerate(retrieved_docs[:MAX_DEBUG_CHUNKS], 1):
                                    source = doc.metadata.get('source', 'Unknown')
                                    filename = extract_filename(source)
                                    st.write(f"**Chunk {i}** (Source: `{filename}`):")
                                    
                                    preview = doc.page_content[:MAX_CHUNK_PREVIEW_LENGTH]
                                    if len(doc.page_content) > MAX_CHUNK_PREVIEW_LENGTH:
                                        preview += "..."
                                    st.text(preview)
                                    st.divider()
                    
                    logger.debug(f"Query: {prompt}, Retrieved {len(result.get('source_documents', []))} documents")
                
                except FileNotFoundError as e:
                    response = (
                        "The vector database could not be found. "
                        "Please ensure the FAISS index is built."
                    )
                    st.error(f"File not found: {str(e)}")
                    logger.error(f"FileNotFoundError: {e}")
                
                except ConnectionError as e:
                    response = (
                        "Could not connect to the LLM service. "
                        "Please ensure Ollama is running."
                    )
                    st.error(f"Connection error: {str(e)}")
                    logger.error(f"ConnectionError: {e}")
                
                except ValueError as e:
                    response = (
                        "There was an error loading the RAG system. "
                        "Please check the configuration."
                    )
                    st.error(f"Configuration error: {str(e)}")
                    logger.error(f"ValueError: {e}")
                
                except Exception as e:
                    response = (
                        "Sorry, I encountered an unexpected error. "
                        "Please try again or rephrase your question."
                    )
                    st.error(f"Error: {str(e)}")
                    logger.exception("Unexpected error occurred")
            
            st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        # Update chat history for the chain (format: list of tuples)
        st.session_state.chat_history.append((prompt, response))


# ============================================================================
# Application Entry Point
# ============================================================================

if __name__ == "__main__":
    # Initialize the chain and retriever
    try:
        chain, retriever = load_chain()
        main()
    except FileNotFoundError as e:
        st.error(f"❌ {str(e)}")
        st.stop()
    except Exception as e:
        st.error(f"❌ Failed to initialize the chatbot: {str(e)}")
        logger.exception("Failed to initialize application")
        st.stop()
