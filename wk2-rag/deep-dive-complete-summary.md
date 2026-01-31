# Deep Dive Complete Summary

**Week 3 — Project 2 RAG Chatbot Deep Dive**

This session walks through building a RAG (Retrieval-Augmented Generation) customer support chatbot from scratch: loading PDFs, chunking, embedding, indexing with FAISS, retrieving, and generating answers with Ollama + LangChain. The second half is a wide-ranging Q&A covering images in PDFs, SQL/structured data, scaling, fine-tuning, deployment, and production best practices.

---

## Key Takeaways

- **RAG pipeline**: Parse → Chunk → Embed → Index → Retrieve → Generate
- **Embedding model is independent of LLM**; no parity concern; retrieval returns text, not vectors
- **Dedicated embedding models** outperform LLM embedding layers for retrieval
- **Production**: swap Ollama for vLLM, use production vector DB, consider agent skills for dynamic prompts
- **Agents** are preferred over static RAG for dynamic, tool-using tasks; retrieval still used inside agents

---

## Session Context and Project Overview

### Week 3 and Project 3
- Deep dive of Project 2 (RAG chatbot)
- Week 3 content includes agents
- Project 3: "Ask the Web" agent (Perplexity-like) for tool calling
- Project 3: latest LangChain, optional MCP, UV or Conda

### RAG Architecture
- RAG = LLM + retrieval system
- Retrieval: given documents (PDFs, images), find relevant chunks for the query, pass to LLM
- Knowledge store = documents unique to the company/use case

---

## Document Loading and Parsing

### Loaders
- **PyPDFLoader** for PDFs; LangChain supports many loaders (search docs for latest)
- Result: 8 PDF pages from 4 Everstorm PDFs (payment, sizing, returns, shipping)
- Optional: WebBaseLoader for URLs; same pattern, different loader
- Use fallbacks when loading fails

### Complex Layouts (PDFs with Tables, Images)
- AI-based parsers in two phases: (1) layout detection (bounding boxes, entity types: text, figure, table, image); (2) structured extraction
- Handle text, images, tables separately; extract text blocks with coordinates
- Instructor will share document parsing resources
- Evaluation: bounding-box metrics, classification accuracy; end-to-end TBD

---

## Chunking

### Text Splitters
- **Recursive Character Text Splitter** preferred: starts from largest coherent units (paragraphs → sentences) until chunk size
- Length-based splitters can break meaning mid-sentence
- **Chunk overlap**: helps avoid splitting important context; experiment for best settings

### Why Overlap Helps
- Reduces risk of splitting mid-sentence/paragraph
- Overlap adds redundancy when a split is unlucky

---

## Embedding and Indexing

### Embedding Models
- Map text → high-dimensional vectors (e.g., 384 dims)
- Similar meaning → nearby in embedding space → enables nearest-neighbor search
- **Why dedicated embedding models**: (1) trained for similarity, not next-token prediction; (2) full transformer vs. single lookup in LLM
- LLM embedding layers: not comparable for retrieval
- **Sentence Transformers** / Hugging Face: `HuggingFaceEmbeddings`, `embed_query()`

### Vector vs. Text Search
- Vector: good for vague/semantic queries
- Keyword: good for specific terms, names, IDs
- **Hybrid** common in production; run both when unsure

### Multimodal Embeddings
- **Images in PDFs**: (1) CLIP or similar (shared text+image space), or (2) image → caption → text embedding
- **Video/Audio**: caption/transcript → text embedding (simpler); or modality-specific embedding models (BLIP, etc.)
- YouTube: text-based search on transcripts/captions

### Embedding Model Independence
- Embedding model fully independent of LLM
- Retrieval returns text chunks; LLM only sees text, never vectors
- No parity concern between embedding and generation models

### Switching Embedding Models
- No way to convert old embeddings to new model
- Must reindex; cost often negligible for typical RAG knowledge bases

---

## Vector Store (FAISS)

### Setup
- `FAISS.from_documents(chunks, embedding_model)` — embeds and builds index
- `vector_db.save_local("faiss_index")` — `.pkl` + `index.faiss`
- Load at inference; no need to re-index each run

### Retrieval
- `vector_db.as_retriever(search_kwargs={"k": 8})` — top 8 chunks
- Optional `score_threshold` for outlier queries
- `get_relevant_documents(query)`

### Index Concept
- Table: IDs + vectors (chunk ↔ embedding)
- FAISS uses specialized structures for fast search
- Inverse index for document ↔ vector mapping; supports updating specific documents

### Persistence and Scale
- FAISS advanced docs cover persistence and loading
- Supports billions of vectors; not necessarily in-memory

---

## LLM (Ollama)

### Setup
- `ollama serve` in separate terminal
- `ollama pull gemma2:1b`
- `ChatOllama(model="gemma2:1b")`
- `llm.invoke(messages)`

### Model Choice
- Gemma 1B minimal; prefer 3B or 7B for real apps
- Embedding: small model used; consider larger Sentence Transformers or Ollama embedding models

---

## RAG Chain Implementation

### Components
- Retriever, LLM, system prompt template with `{context}` and `{question}`

### Workflow
1. `docs = retriever.get_relevant_documents(question)`
2. Format docs: `"\n\n".join(d.page_content for d in docs)`
3. `prompt.format_messages(context=..., question=...)`
4. `answer = llm.invoke(messages)`

### Template
- Static instructions + dynamic context and question
- `ChatPromptTemplate.from_template()` from LangChain

### When Answers Are Wrong
- Inspect retrieved docs: was the right chunk retrieved?
- If not: improve embedding model
- If yes: LLM error; try larger model or better prompting
- Retrieval (FAISS) generally trusted

### Citations
- Optionally return `source_documents` with the answer

---

## UI and Demo

- Streamlit (or Gradio) wraps same logic
- Next project: Chainlit (chainlit.io) for LLM/agent UIs

---

## Q&A: Specialized Data and Use Cases

### SQL / Structured Data
- Use **SQL-specialized embedding models**; general-purpose may underperform
- LLM: 10B+ params often enough; no need for SQL-only LLM
- Local run = fully private

### RAG for Domain-Specific Knowledge (e.g., Distributed Systems)
- Community moved to **agents** for such tasks
- Agents: LLM + tools; coding agents = agents
- RAG for static knowledge; agents for dynamic, tool-using workflows

### Combining Retrieval, Fine-Tuning, Prompt Engineering
- Retrieval used in RAG, agents, coding agents
- Fine-tuned LLM + retrieval (e.g., codebase retrieval) is common

### Web Search in Capstone
- Add web search as tool; covered in guided learning (agents)
- Project 3: web search tool; LLM decides when to use it

---

## Q&A: Fine-Tuning

### When to Fine-Tune
- Custom domain (e.g., medical)
- Behavior/style (shorter answers, tone)
- Inject knowledge the model lacks

### When to Use RAG
- Data can be retrieved and provided as context; avoids fine-tuning cost

### LoRA, RAFT
- **RAFT**: RAG-specific; train LLM to handle noisy retrieved content; rarely used now (agents/thinking models handle it)
- Fine-tuning cost: days/weeks for large setups; hours for small; sometimes minutes (e.g., DreamBooth)
- Local fine-tuning: feasible for small models on strong machines; larger models need cloud (Together, Replicate, etc.)

---

## Q&A: Production and Scale

### Scaling Indexing
- Incremental updates; don’t reindex everything
- Reindex only when embedding model changes

### Scaling Retrieval
- Approximate nearest neighbor (FAISS) for large indexes
- Hybrid vector + keyword search

### Throughput
- Add GPUs; batch requests; distribute across GPUs (RunAI, vLLM)
- **LLM is the bottleneck**; embedding/retrieval usually not

### Deployment
- Replace Ollama with **vLLM** for production
- Use production vector DB (Pinecone, etc.)
- FastAPI or similar for API layer
- Links in repo for serving/deployment

### Vector Databases
- Instructor will share production tool list on course portal
- Chroma, Qdrant, Pinecone, others

---

## Q&A: Evaluation and Guardrails

### Evaluation
- Embedding: recall, precision
- LLM: separate evaluation
- End-to-end: LLM-as-judge; compare predicted vs. ideal output
- Open-source: OpenAI Evals; LangSmith for observability

### Guardrails
- Input/output filtering; often LLM-based (fine-tuned or instructed)

### Query Expansion
- Improve vague or grammatically poor queries before retrieval

---

## Q&A: Prompt and Token Cost

### System Prompt Size
- Larger prompts = more tokens = higher cost
- Balance: enough context vs. unnecessary detail

### Agent Skills
- Store expertise in files; agent loads relevant skills when needed
- Avoid huge static system prompt
- Used by OpenAI, Anthropic, and others

---

## Q&A: User Uploads and Memory

### Uploaded PDFs
- Content appended to context; not added to knowledge base
- New session: no access to previous uploads

### Memory
- Chat history; retrieval from past conversations for recall

---

## Q&A: Document Updates and Reindexing

### When to Reindex
- Depends on use case, budget, compute
- ~90% of cases: reindex when content changes
- Minor additions: index only new content
- Do updates offline; test before rollout

---

## Q&A: Miscellaneous

### Google Colab
- Possible; need to configure Ollama; search for setup

### Project Dependencies
- Each project has its own environment; Project 3 uses newer LangChain, MCP
- UV: faster setup (~30 seconds)

### Lifecycle Management
- No known end-to-end platform for library/dependency lifecycle
- Manual monitoring; evaluate migrations case by case

### Context and Question in Prompt
- Both filled at runtime; context = retrieved docs, question = user input
