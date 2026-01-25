# Review Session Part 1 Summary

## Logistics and Course Updates

### Week 2 Content Release
- Week 2 content has been released
- Guided learning focuses on RAG (Retrieval-Augmented Generation)
- Topics covered:
  - Adapting LLMs
  - Fine-tuning vs RAG
  - Prompt engineering
  - RAG with retrieval and generation

### Project 2 Release
- Customer support chatbot project
- Includes:
  - Python Jupyter Notebook
  - Environment configuration
  - Sample data for getting started
- Key differences from Project 1:
  - Runs locally (not on Colab)
  - Uses lightweight models
  - Uses higher-level packages (LangChain, etc.)

### Installation Notes
- Environment YAML file provided
- Dependencies are pinned for reproducibility
- Optional: UV for faster installation
- Recommendation: Stick with provided versions initially
- Note: LangChain v1 available but project uses v0.x for learning

### Capstone Project
- Guidelines and announcement sent
- Capstone wheel sheet available (main dashboard)
- Past cohort projects available for inspiration

## Project 1 Deep Dive: Tokenization

### Overview
- Project 1 focuses on understanding neural network mechanics
- Covers tokenization, neural network architecture, and GPT-2 inspection
- Run locally for demonstration

### Environment Setup
- Conda environment: `llm_playground`
- Sanity check: Verify package versions match requirements
- IDEs mentioned: VS Code, Cursor, Cursor (anti-gravity)

### Tokenization Fundamentals

#### Purpose
- Neural networks and LLMs don't handle text directly
- Everything must be converted to numbers/mathematical expressions
- Tokenization converts text to numbers

#### Two Phases
1. **Training Phase**: Build vocabulary and mappings
   - Create vocabulary from corpus
   - Build mappings: text chunks → IDs and IDs → text chunks
2. **Inference Phase**: Use tokenizer to encode/decode
   - Encode: text → sequence of numbers
   - Decode: sequence of numbers → text

#### Tokenizer Categories
- **Word Level**: Split by whitespace
- **Character Level**: Split by individual characters
- **Subword Level**: Most common in modern LLMs (BPE, etc.)

### Word Level Tokenizer Implementation

#### Steps
1. **Corpus Processing**
   - Sample corpus provided (toy example)
   - In practice: trillions of words/tokens

2. **Text Chunking**
   - Split by whitespace
   - Standardize: convert to lowercase
   - Example: "Perfectly fine" → ["perfectly", "fine"]

3. **Vocabulary Building**
   - Collect all chunks from corpus
   - Remove duplicates (use set)
   - Sort alphabetically

4. **Mapping Creation**
   - **Word to ID**: Dictionary mapping words to indices
   - **ID to Word**: Dictionary mapping indices to words
   - IDs are sequential (0, 1, 2, ...)

5. **Special Token: Unknown**
   - Problem: Unknown words at inference time
   - Solution: Add `<UNK>` special token
   - Use when word not in vocabulary

6. **Encode Function**
   - Split input text
   - Convert to lowercase
   - Map each word to ID (use `<UNK>` if not found)
   - Return sequence of IDs

7. **Decode Function**
   - Map each ID to word
   - Join with whitespace
   - Return text

#### Limitations
- Unknown words become `<UNK>` and lose information
- Cannot distinguish between different unknown words
- Vocabulary size can explode with many unique words

### Character Level Tokenizer Implementation

#### Differences from Word Level
- No whitespace splitting
- Iterate over all characters in string
- Vocabulary: All ASCII letters (lowercase + uppercase)
- Can add punctuation if needed

#### Implementation
- Use `string.ascii_lowercase` and `string.ascii_uppercase`
- Add `<UNK>` special token
- Similar encode/decode logic but character-based
- Join without whitespace in decode

#### Limitations
- Loses unknown characters (punctuation, emojis, etc.)
- Longer sequences (one token per character)

### Subword Level Tokenizer (BPE)

#### Overview
- Used by almost all modern LLMs
- Not heuristic-based like word/character level
- Learns optimal subword units from corpus

#### BPE Algorithm
1. Start with all characters in vocabulary
2. Iteratively merge most frequent token pairs
3. Continue until vocabulary reaches target size
4. Examples:
   - GPT-2: 50,257 tokens
   - GPT-3/4: 100,000 tokens
   - Recent models: 200,000 tokens

#### Implementation with GPT-2
- Use Hugging Face Transformers library
- Load GPT-2 tokenizer: `AutoTokenizer.from_pretrained("gpt2")`
- Vocabulary size: 50,257 tokens
- Special token: `<|endoftext|>` (end of text marker)

#### Advantages
- Handles unknown words (splits into subwords)
- More efficient vocabulary size
- Better for multilingual text
- No `<UNK>` token needed (works at byte level)

#### Special Characters and Emojis
- BPE works at byte level (UTF-8 encoding)
- Emojis become multiple bytes → merged into tokens
- Tokenizer doesn't "know" it's an emoji, just sees frequent byte patterns

### Tiktoken Library

#### Overview
- Production-ready library by OpenAI
- Provides access to OpenAI's trained tokenizers
- Common tokenizers:
  - `cl100k_base`: Used for GPT-4, GPT-4 Turbo, GPT-3.5 Turbo
  - `o200k_base`: Used for GPT-4o family
  - Older versions available

#### Usage
- `tiktoken.get_encoding("cl100k_base")`
- Simple encode/decode interface
- Same functionality as Hugging Face tokenizers

### Key Takeaways
- Tokenization is fundamental: text → numbers
- Word/character level: simple but limited
- BPE: industry standard, handles unknowns better
- Vocabulary size is a hyperparameter
- Token IDs are sequential (0, 1, 2, ...)


