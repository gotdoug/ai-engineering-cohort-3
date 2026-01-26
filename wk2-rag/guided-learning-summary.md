# Complete RAG and LLM Adaptation Summary

## Overview
- Goal: Adapt general-purpose LLMs for domain-specific use cases using additional documents
- Three main techniques: Fine-tuning, Prompt Engineering, and RAG (Retrieval Augmented Generation)
- Documents can be: PDFs, images, HTMLs, Wiki pages, etc.

## Why Adaptation is Needed

### General Purpose LLM Limitations
- Works well for: Math questions, brainstorming, coding questions (seen in training data)
- Fails for domain-specific questions:
  - Example: Retail store chatbot asks "What is your refund policy?"
  - Problem: LLM hallucinates or gives incorrect answers (e.g., assumes question is about OpenAI)
  - Need: Adapt LLM to use internal documents/knowledge base

### Problem Statement
- Adapt a general-purpose LLM to accurately answer questions in a specific domain using additional documents
- Example: Customer asks "What is the refund policy?" → LLM should answer based on document database

## Three Techniques for LLM Adaptation

### 1. Fine-Tuning

#### Concept
- Continue training general-purpose LLM on document database
- Output: Specialized LLM with tuned weights
- Answers come from learned weights (compressed knowledge of training data)

#### Approaches

##### Full Parameter Fine-Tuning
- Update all weights in the LLM
- Problem: Computationally very expensive (billions of parameters)

##### Parameter Efficient Fine-Tuning (PEFT)
- Only update a subset of parameters
- Techniques:
  - **Adapters**
    - Freeze original LLM parameters
    - Inject new trainable layers into transformer architecture
    - Only adapter layers are learned during fine-tuning
    - Paper: "Parameter Efficient Transfer Learning for NLP" (2019)
  - **LoRA (Low-Rank Adaptation)**
    - Freeze original linear layer weights
    - Add two low-rank matrices (A and B) as parallel branch
    - Output: Wx + ABx (where ABx has same shape as Wx)
    - Only the two new matrices are learnable
    - Advantages: Faster at inference time than adapters
    - Paper: "LoRA: Low-Rank Adaptation of Large Language Models"
  - Other: Prompt tuning, activation scalers, sparse weight deltas

##### Implementation
- Library: Hugging Face PEFT
- Example: Cohere 2.5B model → Only ~0.1% parameters trainable (3M out of 3B)
- Workflow: Load model → Create LoRA config → Wrap with PEFT → Train → Save/load

### 2. Prompt Engineering

#### Concept
- Craft or design prompts to extract desired output from LLM
- Workflow: User query → Prompt Engineering (modifies/adds to query) → Enhanced prompt → LLM → Response

#### Techniques

##### Few-Shot Prompting
- Show examples to the model in the prompt
- Model follows the format of the examples
- Works even with base models (continuation models)
- Can control output format

##### Zero-Shot Prompting
- No examples shown, still guides generation
- Simple changes like adding "Q:" and "A:" labels
- Can enforce structured output (e.g., JSON format)

##### Chain of Thought (CoT) Prompting
- Most popular technique
- Shows model how to reason step-by-step
- Variants:
  - **Few-shot CoT**: Show examples with reasoning traces
    - Paper: "Chain of Thought Prompting" (Google Brain, Jan 2023)
    - Performance: Solve rate improved from 18% to 57% on math problems
  - **Zero-shot CoT**: Just add "Let's think step by step"
    - Paper: "Zero-Shot Chain of Thought" (Google Brain, Jan 2023)
- Foundation for thinking models

##### Role-Specific Prompting
- Assign a role to the LLM (e.g., "You are an expert tax advisor")
- Simple but effective improvement

#### Prompt Structure
- **System Prompt**: Hidden instructions (roles, examples, chain of thought, etc.) - set once, used for all queries
- **User Prompt**: Visible query that user types

#### Limitations
- Approach: Include all internal documents in system prompt
- Problem: Context window limitation
  - LLMs have maximum context length
  - Thousands/millions of PDFs exceed practical limits
  - Computationally expensive or impossible
- Solution: Works for small document sets, but not scalable

### 3. RAG (Retrieval Augmented Generation)
- Solves the context window limitation of prompt engineering
- Two main components: Retrieval and Generation
- Adds retrieval component to find only relevant documents instead of including all

## RAG System: Building the Index (Offline Preprocessing)

### Step 1: Document Parsing
- Convert documents (PDFs, HTMLs) to extracted text content
- Methods:
  - **Rule-based**: Less common, not popular
  - **Deep learning-based models**: More common
    - Process:
      1. Layout detection (identify titles, text, figures, tables)
      2. Text extraction (extract text from detected layouts)
    - Output: Structured output with text blocks
    - For images: Include coordinates for later indexing
- Libraries:
  - **Unstructured.io**: Automates document parsing
  - **LayoutParser**: Unified toolkit for document image analysis (detects images, layout, extracts text using OCR)

### Step 2: Document Chunking
- Break documents into smaller, manageable pieces (chunks)
- Reasons:
  - Documents may be too broad (entire books/reports)
  - May exceed context window
  - Need uniform chunk sizes
- Advantages:
  - Handle non-uniform document sizes
  - Improve precision (find specific relevant pieces)
  - Overcome context window limitations
  - Optimize computational resources
- Algorithms:
  - **Length-based**: Split by specified length (problem: may split mid-sentence)
  - **Regular expression-based**: Split by punctuation (better: doesn't split mid-sentence, but lacks semantic understanding)
  - **Semantic splitters**: Use specialized models (recommended)
    - Split at semantic boundaries (headers, items, code blocks)
    - Example: LangChain's text splitters
- Hyperparameters:
  - Chunk size (e.g., 512 characters)
  - Overlap (e.g., 50 characters) to avoid cutting mid-topic

### Step 3: Indexing
- Store chunks in data structure that is easy to search
- Methods:
  - Keyword-based indexing
  - Full-text indexing (e.g., Elasticsearch)
  - Knowledge graph-based indexing
  - **Vector-based indexing** (most common - 90-95% of use cases)

#### Vector-Based Indexing
- Use embedding models to encode text into vectors
- **Embedding Models**:
  - Map text to high-dimensional vector space (embedding space)
  - Training: Similar meanings → nearby in embedding space
  - Historical paper: Word2Vec (showed semantic relationships)
  - Examples: OpenAI text-embedding-3-large (3,072 dimensions)
- Process:
  - Map each chunk to a vector
  - Store in index table (chunk ID + embedding vector)
  - Similar chunks have nearby vectors

#### Handling Images
- Two options:
  1. **Image Embedding Models** (e.g., CLIP)
    - Use shared embedding space (same encoder for text and images)
    - Important: Use same text encoder for text chunks
    - Build separate image index
  2. **Image Captioning Models**
    - Generate text caption from image
    - Use text encoder on caption
    - Simpler but less direct
- Result: Two indices (text index and image index)

## RAG System: Search/Retrieval (Runtime)

### Process
1. Encode user query using same text encoder → query embedding vector
2. Find embeddings in index that are most similar to query embedding
3. Return corresponding text chunks
- Similarity measures: Euclidean distance, cosine distance

### Nearest Neighbor Search
- Problem: Given points in high-dimensional space + query point, find top k nearest points
- Two categories:

#### Exact Nearest Neighbor
- Guarantees exact top k closest points
- Problem: Computationally expensive (millions/billions of data points in RAG systems)

#### Approximate Nearest Neighbor (ANN)
- Returns reasonably close points (may not be exact top k)
- Trade-off: Sacrifice some accuracy for efficiency
- Categories:
  - **Clustering-based**: Cluster points, find query's cluster, search only within cluster
  - **Tree-based**: Partition data space, form tree structure, traverse to find region, search within region
  - **Locality Sensitive Hashing (LSH)**: Hash function maps similar inputs to similar outputs, search only in query's bucket
  - **Graph-based**: (not covered in detail)
- Libraries: FAISS (Facebook AI Similarity Search)

### Workflow
1. User query → Text encoder → Query embedding
2. Search algorithm (e.g., clustering-based):
   - Find cluster query belongs to
   - Intra-cluster search: Find closest points within cluster
3. Return retrieved chunks (retrieve_doc_1, retrieve_doc_2, ..., retrieve_doc_k)

## RAG System: Generation Component

### Basic Generation
- Core: General-purpose LLM
- Process:
  1. Retrieve content from retrieval component
  2. Combine with user query
  3. Form prompt
  4. LLM generates output

### Enhanced Generation
- Combine with prompt engineering techniques
- Workflow:
  1. Retrieved content + user query → Prompt engineering
  2. Prompt engineering adds:
     - Role-specific prompting
     - Few-shot examples
     - Chain of thought
     - Instructions (e.g., "deliver concise and accurate response")
  3. Enhanced prompt → LLM → Response

### Improving Generation Quality: RAFT
- Problem: If retrieved items are inaccurate/irrelevant, LLM may fail
- Solution: **RAFT (Retrieval Augmented Fine-Tuning)**
  - Fine-tune LLM to distinguish relevant vs irrelevant documents
  - Process:
    - Label documents as relevant/irrelevant
    - Continue training LLM
    - LLM learns to rely more on relevant documents, ignore irrelevant ones
  - Paper: Published in 2024
  - Combines: Fine-tuning + Prompt Engineering + RAG

## Evaluation of RAG Systems

### Complexity
- Multiple components → complex evaluation
- Different aspects to measure

### Key Evaluation Aspects

#### 1. Context Relevance
- Measures: How accurately retrieval component selects relevant documents
- Between: Query and Context
- Metrics: Ranking metrics
  - Hit rate
  - MRR (Mean Reciprocal Rank)
  - NDCG (Normalized Discounted Cumulative Gain)
  - Precision@k

#### 2. Faithfulness
- Measures: If generated response is faithful to provided context
- Between: Result and Context
- Problem: Generated response may hallucinate or differ from context
- Evaluation: Subjective, often requires humans
- Tools: Fact-checking tools, consistency checks

#### 3. Answer Relevance
- Measures: If generation is relevant to the query
- Between: Result and Query
- Metrics: Similar to caption generation systems
- Compare: Generated response vs correct response

#### 4. Answer Correctness
- Measures: If result is correct given the query
- Between: Result and Query
- Metrics: Sentence/paragraph similarity metrics

## Complete RAG System Design

### Indexing Process (Offline)
1. Document database (PDFs, HTMLs, etc.)
2. Document parsing → Extract text/images
3. Document chunking → Smaller pieces
4. Apply encoders:
   - Text encoder → Text index
   - Image encoder → Image index
5. Result: Two indices (text and image) with chunk IDs and embeddings

### Runtime Process (Online)
1. **Input Guardrails**: Ensure safe requests
2. **Query Rewrite/Expansion**: Improve/enhance user query
   - Fix ambiguities, missing punctuation, grammatical issues
3. **Text Encoder**: Get query embedding
4. **Nearest Neighbor Search**: Find relevant chunks (text or image)
5. **Prompt Engineering**: Combine retrieved content + user query
   - Add role-specific, few-shot, chain of thought
6. **LLM**: Process enhanced prompt → Generate response
7. **Output Guardrails**: Ensure safe output

### Key Benefits
- Easy to add new documents: Just index them
- Can incorporate live data (future topic: tool calling and search)
- Combines multiple techniques (fine-tuning, prompt engineering, RAG) for best results

