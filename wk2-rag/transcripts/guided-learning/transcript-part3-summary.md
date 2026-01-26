# Transcript Part 3 Summary

## Search/Retrieval from Index

### Overview
- Once index is built, need to search it at runtime
- Problem: Given user query, find most relevant chunks from index

### Process
1. Encode user query using same text encoder → query embedding vector
2. Find embeddings in index that are most similar to query embedding
3. Return corresponding text chunks
- Similarity measures: Euclidean distance, cosine distance

### Nearest Neighbor Search
- Traditional computer science problem
- Given: Points in high-dimensional space + query point
- Goal: Find top k nearest points

### Two Categories of Algorithms

#### 1. Exact Nearest Neighbor
- Guarantees exact top k closest points
- Problem: Computationally expensive
  - Millions/billions of data points in RAG systems
  - Comparing query to billions of points is too slow

#### 2. Approximate Nearest Neighbor (ANN)
- Returns reasonably close points (may not be exact top k)
- Trade-off: Sacrifice some accuracy for efficiency
- Four main categories:
  - **Clustering-based**:
    - Cluster all points
    - Find which cluster query belongs to
    - Search only within that cluster
    - Example: Query in cluster 1 → search only cluster 1 points
  - **Tree-based**:
    - Partition data space into subspaces
    - Form tree structure with leaf nodes (regions)
    - Traverse tree to find region
    - Search only within that region
  - **Locality Sensitive Hashing (LSH)**:
    - Hash function: Similar inputs → similar hash outputs
    - Preprocessing: Apply hash to all data points → assign to buckets
    - Query: Hash query → search only in that bucket
  - **Graph-based**: (not covered in detail)

### Workflow
1. User query → Text encoder → Query embedding
2. Search algorithm (e.g., clustering-based):
   - Find cluster query belongs to
   - Intra-cluster search: Find closest points within cluster
3. Return retrieved chunks (retrieve_doc_1, retrieve_doc_2, ..., retrieve_doc_k)
- Libraries: FAISS (Facebook AI Similarity Search) - efficient similarity search and clustering

## Generation Component

### Basic Generation
- Core: General-purpose LLM
- Process:
  1. Retrieve content from retrieval component
  2. Combine with user query
  3. Form prompt
  4. LLM generates output

### Enhanced Generation
- Combine with prompt engineering
- Workflow:
  1. Retrieved content + user query → Prompt engineering
  2. Prompt engineering adds:
     - Role-specific prompting
     - Few-shot examples
     - Chain of thought
     - Instructions (e.g., "deliver concise and accurate response")
  3. Enhanced prompt → LLM → Response

### Improving Generation Quality
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
- Combines multiple techniques for best results

