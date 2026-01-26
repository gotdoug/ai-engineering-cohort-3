# Transcript Part 2 Summary

## Prompt Engineering

### Concept
- Way to craft or design prompts to extract desired output from LLM
- Workflow: User query → Prompt Engineering (modifies/adds to query) → Enhanced prompt → LLM → Response

### Techniques

#### 1. Few-Shot Prompting
- Show examples to the model in the prompt
- Model follows the format of the examples
- Example: Q&A format with examples, then actual question
- Works even with base models (continuation models)
- Can control output format

#### 2. Zero-Shot Prompting
- No examples shown
- Still guides generation process
- Simple changes like adding "Q:" and "A:" labels
- Can enforce structured output (e.g., JSON format)
- Example: "Return only JSON in this format: {years_experience: number}"

#### 3. Chain of Thought (CoT) Prompting
- Most popular technique
- Shows model how to reason step-by-step
- Two variants:
  - **Few-shot CoT**: Show examples with reasoning traces
    - Paper: "Chain of Thought Prompting" (Google Brain, Jan 2023)
    - Example: Math problem with step-by-step solution shown
    - Performance: Solve rate improved from 18% to 57% on math problems
  - **Zero-shot CoT**: Just add "Let's think step by step"
    - Paper: "Zero-Shot Chain of Thought" (Google Brain, Jan 2023)
    - Simple but effective
- Foundation for thinking models (future topic)

#### 4. Role-Specific Prompting
- Assign a role to the LLM
- Example: "You are an expert tax advisor"
- Simple but effective improvement

### Prompt Structure
- Two components:
  - **System Prompt**: Hidden instructions (roles, examples, chain of thought, etc.)
  - **User Prompt**: Visible query that user types
- System prompt makes things organized (set once, used for all queries)

### Using Prompt Engineering for Domain Adaptation
- Approach: Include all internal documents in system prompt
- Example: "Read the following documents and respond to the question" + all PDFs/knowledge base
- Problem: Context window limitation
  - LLMs have maximum context length
  - Thousands/millions of PDFs exceed practical limits
  - Computationally expensive or impossible
- Solution: Works for small document sets, but not scalable

## Introduction to RAG (Retrieval Augmented Generation)
- Third technique for adapting LLMs
- Solves the context window limitation of prompt engineering
- Adds retrieval component to find only relevant documents
- Two main components: Retrieval and Generation

## Building a Searchable Index

### Overview
- Two steps:
  1. Build searchable index from documents (preprocessing)
  2. Search from index at runtime (when query comes)

### Step 1: Document Parsing
- Convert documents (PDFs, HTMLs) to extracted text content
- Two methods:
  - **Rule-based**: Less common, not popular
  - **Deep learning-based models**: More common
    - Process:
      1. Layout detection (identify titles, text, figures, tables)
      2. Text extraction (extract text from detected layouts)
    - Output: Structured output with text blocks
    - For images: Include coordinates for later indexing
- Libraries:
  - **Unstructured.io**: Automates document parsing
  - **LayoutParser**: Unified toolkit for document image analysis
    - Can detect images, layout, extract text using OCR
    - Works with PDFs, magazines, websites, historical documents

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
  - **Length-based**: Split by specified length
    - Problem: May split in middle of sentences
  - **Regular expression-based**: Split by punctuation
    - Better: Doesn't split mid-sentence
    - Problem: Lacks semantic understanding
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
  - Full-text indexing
  - Knowledge graph-based indexing
  - **Vector-based indexing** (most common - 90-95% of use cases)

#### Text-Based Indexing
- Match partial or exact query terms with document content
- Example: Elasticsearch
- Problem: Doesn't capture semantic meaning
  - Can't handle synonyms
  - No semantic understanding

#### Vector-Based Indexing
- Use embedding models to encode text into vectors
- **Embedding Models**:
  - Map text to high-dimensional vector space (embedding space)
  - Training: Similar meanings → nearby in embedding space
  - Historical paper: Word2Vec (showed semantic relationships)
  - Examples:
    - OpenAI text-embedding-3-large (3,072 dimensions)
    - Many other models available
- Process:
  - Map each chunk to a vector
  - Store in index table (chunk ID + embedding vector)
  - Similar chunks have nearby vectors

#### Handling Images in Indexing
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

