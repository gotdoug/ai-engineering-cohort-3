# Review Session Part 3 Summary

## Text Generation and Decoding Strategies

### Generation Implementation

#### Using Hugging Face Generate
- Simple one-line call: `model.generate(input_ids)`
- Handles entire generation loop automatically
- Parameters:
  - `max_new_tokens`: Maximum tokens to generate (e.g., 80)
  - `do_sample`: Enable/disable sampling
  - `top_k`: Number of top tokens to consider
  - `top_p`: Nucleus sampling threshold

#### Generation Examples
- **Prompt**: "Once upon a time"
  - GPT-2: Generates story continuation
  - Quality varies with model size
  
- **Prompt**: "What is 2+2?"
  - GPT-2: Poor answer (treats as continuation)
  - Qwen: Correct answer ("4")

### Decoding Strategies Comparison

#### Greedy Decoding
- Always picks highest probability token
- `do_sample=False`
- Deterministic but can be repetitive
- Fast but less creative

#### Top-k Sampling
- Considers top k tokens
- Samples from this subset
- `do_sample=True, top_k=50`
- More diverse outputs
- Ignores very unlikely tokens

#### Top-p (Nucleus) Sampling
- Considers tokens until cumulative probability ≥ p
- Dynamic token set size
- `do_sample=True, top_p=0.9`
- Balances diversity and quality

### Model Comparison: GPT-2 vs Qwen

#### GPT-2
- 117M parameters
- Early model (2019)
- Limited capabilities
- Struggles with reasoning tasks

#### Qwen 3
- 600M parameters
- More recent model
- Better performance
- Handles reasoning better

#### Key Insight
- Same architecture, different sizes
- Easy to swap models
- Interface remains the same
- Larger models = better results

### How LLMs Work (Summary)

#### End-to-End Flow
1. **Input**: User prompt (text)
2. **Tokenization**: Text → token IDs
3. **Embedding**: IDs → embedding vectors
4. **Transformer**: Process through layers
5. **Output**: Probabilities for next token
6. **Decoding**: Select next token
7. **Repeat**: Append and continue
8. **Stop**: End token or max length

#### Key Components
- **Tokenizer**: Converts text ↔ numbers
- **Embeddings**: Convert IDs to vectors
- **Transformer**: Sequence of layers (attention + feed-forward)
- **LM Head**: Final layer (vocab_size output)
- **Decoding**: Strategy to select tokens

### Q&A Session Highlights

#### Tokenization Questions

**Q: Are token IDs always sequential?**
- Yes, IDs are sequential (0, 1, 2, ...)
- Based on index in vocabulary
- No randomness in ID assignment

**Q: How do unknown tokens work?**
- Word/character level: Use `<UNK>` token
- Problem: Multiple unknown words map to same token
- BPE: No `<UNK>` needed (works at byte level)
- BPE splits unknown words into subwords

**Q: Vocabulary size and vector dimensions?**
- Vocabulary size: Number of unique tokens
- Determines output dimension of LM head
- Embedding dimension: Size of hidden vectors (e.g., 768)
- Different concepts but related

#### Architecture Questions

**Q: Embedding matrix dimensions?**
- Shape: `[vocab_size, hidden_dim]`
- GPT-2: 50,257 × 768
- Each row = embedding for one token
- Lookup table: ID → embedding vector

**Q: How does 768 → 50,257 transformation work?**
- Final linear layer (LM head)
- Weight matrix: 768 × 50,257
- Matrix multiplication transforms dimensions
- One probability per vocabulary token

**Q: Sequence length handling?**
- Variable input lengths
- Padding for shorter sequences
- Max sequence length: 1024 (GPT-2)
- Modern models: 4k, 8k, 32k, millions

#### Normalization Layers

**Q: What is layer normalization?**
- Normalizes activations at each layer
- Prevents values from becoming too large/small
- Helps with training stability

**Q: Why is normalization needed?**
- **Vanishing gradients**: Values too small → gradients disappear
- **Exploding gradients**: Values too large → gradients explode
- Normalization keeps activations in controlled range
- Makes training more stable

**Q: Normalization and similarity search?**
- Normalization used in cosine similarity
- Dot product vs normalized dot product
- Different use cases (popularity bias considerations)
- Recommendation systems context

#### Multi-head Attention

**Q: How do dimensions change in attention?**
- Query, Key, Value matrices
- Each is a linear layer
- Input: `[seq_len, hidden_dim]`
- Output: `[seq_len, hidden_dim]` (usually same)
- Multiple heads: Split hidden_dim across heads

**Q: Weight matrix shapes?**
- Linear layer: `[hidden_dim, hidden_dim]` (if same input/output)
- GPT-2: 768 × 768 for each Q/K/V
- Larger models: 12,288 × 12,288 (GPT-3)

#### Modern Tokenization

**Q: What tokenization do modern models use?**
- Mostly BPE variants
- GPT-4: cl100k_base (100k tokens)
- GPT-4o: o200k_base (200k tokens)
- Still BPE at core, with improvements

**Q: Multilingual tokenization?**
- Vocabulary size increased for multilingual support
- 50k → 100k → 200k
- Includes tokens from multiple languages
- BPE handles languages without spaces (e.g., Chinese)

**Q: Chinese and languages without spaces?**
- BPE works at byte/character level
- Doesn't rely on whitespace
- Works for Chinese, Japanese, etc.
- Frequency-based merging still applies

#### Hyperparameters vs Parameters

**Q: What's the difference?**
- **Parameters**: Weights in model (learnable)
  - Example: 117M parameters in GPT-2
  - Updated during training
- **Hyperparameters**: Design choices (fixed)
  - Example: hidden_dim=768, num_layers=12
  - Set before training, not learned

#### Batch Processing

**Q: Can LLMs handle multiple requests in parallel?**
- Yes, batch processing supported
- First dimension is batch_size
- Send multiple prompts at once
- Model processes batch in parallel
- APIs support batching

#### Context Window Limitations

**Q: Long context and information loss?**
- Models may focus on beginning/end
- Middle content sometimes less influential
- Ongoing research area
- Evaluation tests for long-context recall

**Q: Solutions for long context?**
- RAG (Retrieval-Augmented Generation)
- Dynamic context building
- File-based storage and retrieval
- Tool calling and agentic systems
- MCP (Model Context Protocol)

#### Sequence Length Details

**Q: Variable length inputs?**
- Padding with special tokens
- Truncation if too long
- Max sequence length limit
- Handled during preprocessing

**Q: Ring Attention and long context?**
- Research from Berkeley
- Enables millions of tokens
- Used by modern long-context models
- Allows processing very long documents

#### Understanding Model Internals

**Q: What do the numbers in embeddings mean?**
- Numbers are learned representations
- Not interpretable by humans
- Meaning emerges from training
- Focus on shapes, not individual values

**Q: Inspecting model layers?**
- Can print layer structures
- Inspect weight shapes
- Understand dimensions
- Values themselves not meaningful

### Key Takeaways

#### For Future Projects
- Don't need to understand all details
- Can treat models as black boxes
- Higher-level libraries (LangChain) abstract complexity
- Foundation helps understand technical reports

#### Learning Path
- Project 1: Deep dive into fundamentals
- Project 2+: Use higher-level tools
- Understanding helps but not required for building
- Can revisit details later

#### Modern LLM Development
- Focus on application building
- Use pre-trained models
- Understand high-level concepts
- Details matter for research, less for applications

### Resources Mentioned
- Hugging Face Transformers documentation
- Tiktoken library (OpenAI)
- Ring Attention paper (Berkeley)
- Layer normalization video (Andrej Karpathy)
- Cosine similarity in recommendation systems


