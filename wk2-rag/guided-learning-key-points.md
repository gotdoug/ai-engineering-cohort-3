# RAG & LLM Adaptation — Key Points

Quick reference from the guided learning summary. See `guided-learning-summary.md` for full detail. Project-specific tools from `project_2/rag_chatbot.ipynb`.

## Why adapt LLMs?
- General-purpose LLMs fail on domain-specific questions (hallucinate, give wrong context)
- Need to ground answers in internal documents / knowledge base

## Three adaptation techniques

| Technique | Idea | When |
|-----------|------|------|
| **Fine-tuning** | Train on domain docs; weights encode knowledge | Permanent specialization |
| **Prompt engineering** | Craft prompts, few-shot, CoT, roles | Limited docs, no retraining |
| **RAG** | Retrieve relevant docs at runtime → feed to LLM | Large doc sets, scalable |

## RAG pipeline

### Offline (indexing)
1. **Parse** — Extract text/images from PDFs, HTML, etc. (Unstructured.io, LayoutParser)
2. **Chunk** — Split into smaller pieces (semantic splitters, chunk size + overlap)
3. **Index** — Embed chunks with text encoder → vector index (FAISS, etc.)

### Online (runtime)
1. Encode query → find nearest chunks (ANN search)
2. Retrieved chunks + user query → prompt engineering (role, few-shot, CoT)
3. Enhanced prompt → LLM → response

## Key concepts
- **Embeddings** — Text → high‑dim vectors; similar meaning → nearby vectors
- **ANN** — Approximate nearest neighbor (speed vs exactness)
- **RAFT** — Fine-tune LLM to weight relevant vs irrelevant retrieved docs

## RAG evaluation
- **Context relevance** — Are retrieved docs relevant? (Hit rate, MRR, NDCG, P@k)
- **Faithfulness** — Does output match provided context?
- **Answer relevance** — Does output address the query?
- **Answer correctness** — Is the answer factually correct?

---

## Project 2: tools and technical details

Reference: `project_2/rag_chatbot.ipynb`, env: `project_2/environment.yml`

### Step 2 — Document load & chunk
| Step | Tool | Details |
|------|------|---------|
| **Load PDFs** | `PyPDFLoader` (langchain_community) | `loader = PyPDFLoader(pdf_path)` → `loader.load()`; glob `data/Everstorm_*.pdf` |
| **Load web (opt)** | `UnstructuredURLLoader` | Fetch HTML → extract text |
| **Load TXT** | `TextLoader` | For plain-text docs |
| **Chunk** | `RecursiveCharacterTextSplitter` (langchain) | `chunk_size=300`, `chunk_overlap=30`; keeps paragraph/sentence boundaries |

### Step 3 — Embed & index
| Step | Tool | Details |
|------|------|---------|
| **Embeddings** | `SentenceTransformerEmbeddings` (langchain) | `model_name="thenlper/gte-small"`; local, no API key |
| **Vector store** | `FAISS` (langchain) | `FAISS.from_documents(chunks, embeddings)`; in-memory ANN index |
| **Retriever** | `vectordb.as_retriever()` | `search_kwargs={"k": 8}` → top 8 chunks per query |

### Step 4–5 — LLM & RAG chain
| Step | Tool | Details |
|------|------|---------|
| **LLM** | `Ollama` (langchain_community) | `model="gemma3:1b"`, `temperature=0.1`; local via Ollama server |
| **Prompt** | `PromptTemplate` | `{context}` + `{question}`; instruct “answer only from context,” refuse when not in docs |
| **Chain** | `ConversationalRetrievalChain.from_llm()` | Combines retriever + LLM + prompt; `combine_docs_chain_kwargs={"prompt": prompt}` |

### Step 6 — UI
| Step | Tool | Details |
|------|------|---------|
| **Web UI** | Streamlit | `st.chat_message`, `st.chat_input`, session state for `messages` + `chat_history` |

### Key packages (environment.yml)
- `langchain`, `langchain-community` — loaders, chains, prompts
- `sentence-transformers` — embeddings (gte-small)
- `faiss-cpu` — vector search
- `unstructured` — document parsing
- `streamlit` — chat UI
