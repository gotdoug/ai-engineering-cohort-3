# Review Session Part 2 Summary

## Neural Networks and LLM Architecture

### Neural Networks Overview

#### Basic Concept
- Neural networks are sequences of layers
- Layers operate on mathematical expressions (numbers)
- Input → transformations → output

#### Linear Layer
- **Purpose**: Linear transformation of input to output
- **Components**:
  - Weight matrix (W)
  - Bias term (b)
  - Formula: `output = input × W^T + b`
- **Shape**: Determined by input and output dimensions
  - Example: 3 input features → 2 output features
  - Weight matrix: 3 × 2

#### Implementation
- **PyTorch Class Structure**:
  - `__init__`: Create weights and bias
  - `forward`: Implement computation
- **Weight Initialization**: Random values initially
- **Training**: Weights updated during training via backpropagation

#### PyTorch Built-in
- `nn.Linear`: Pre-implemented linear layer
- No need to implement from scratch in practice
- More reliable and optimized

### Transformer Architecture

#### Overview
- Most LLMs are based on decoder-only transformers
- Original transformer had encoder-decoder (for translation)
- LLMs use decoder-only (for language generation)

#### Architecture Flow
1. Input: Sequence of token IDs
2. Layers: Linear layers and attention layers
3. Output: Probabilities for next token

### GPT-2 Model Inspection

#### Loading GPT-2
- Use Hugging Face Transformers
- `GPT2LMHeadModel.from_pretrained("gpt2")`
- Downloads pre-trained model with weights

#### Model Structure
- **Two Main Components**:
  1. **Transformer**: Core architecture
  2. **LM Head**: Final linear layer (vocabulary size output)

#### Transformer Components

1. **Embeddings**:
   - **Text Embeddings (WTE)**: 
     - Maps token IDs to vectors
     - Shape: vocabulary_size × hidden_dim
     - Example: 50,257 × 768 for GPT-2
   - **Position Embeddings (WPE)**:
     - Adds position information
     - Same hidden dimension (768)
   - **Combined**: Text embeddings + Position embeddings

2. **Transformer Blocks**:
   - **Number**: 12 blocks (h[0] to h[11])
   - **Each Block Contains**:
     - Layer normalization
     - Multi-head attention
     - Layer normalization
     - MLP (feed-forward network)
   - **MLP Structure**:
     - Two linear layers
     - Expands then contracts dimensions
     - Example: 768 → 3072 → 768

3. **LM Head**:
   - Final linear layer
   - Converts hidden dimension to vocabulary size
   - Shape: 768 × 50,257 for GPT-2

### Forward Pass Through GPT-2

#### Step-by-Step Example

1. **Input**: "hello my name"
   - Tokenize → 3 token IDs

2. **Embedding Layer**:
   - Convert IDs to embeddings
   - Add position embeddings
   - Output shape: 3 × 768 (sequence_length × hidden_dim)

3. **Transformer Blocks**:
   - Pass through 12 blocks
   - Each block: attention + feed-forward
   - Output shape: Still 3 × 768

4. **LM Head**:
   - Final linear transformation
   - Output shape: 3 × 50,257 (sequence_length × vocab_size)

5. **Extract Last Token**:
   - Take last vector (for next token prediction)
   - Shape: 50,257 (vocabulary size)

6. **Softmax**:
   - Convert logits to probabilities
   - Shape: 50,257 (probabilities for each token)

7. **Top-k Selection**:
   - Find highest probability tokens
   - Example: "is" with 77% probability

### Text Generation

#### Basic Generation Loop
1. Start with prompt
2. Tokenize prompt → IDs
3. Pass through model → get logits
4. Apply softmax → probabilities
5. Select next token (greedy or sampling)
6. Append to prompt
7. Repeat until end token or max length

#### Implementation with Hugging Face
- `model.generate()`: Built-in generation method
- Handles the loop automatically
- Parameters:
  - `max_new_tokens`: Maximum tokens to generate
  - `do_sample`: Enable sampling (vs greedy)
  - `top_k`: Consider top k tokens
  - `top_p`: Nucleus sampling threshold

### Decoding Strategies

#### Greedy Decoding
- Always pick highest probability token
- Deterministic
- Can be repetitive
- `do_sample=False`

#### Top-k Sampling
- Consider top k most likely tokens
- Sample from this subset
- More diverse outputs
- `do_sample=True, top_k=50`

#### Top-p (Nucleus) Sampling
- Consider tokens until cumulative probability reaches p
- Dynamic token set size
- `do_sample=True, top_p=0.9`

### Model Comparison

#### GPT-2 vs Qwen
- **GPT-2**: 
  - 117M parameters
  - Early model, limited capabilities
  - Example: "What is 2+2?" → poor answer
  
- **Qwen 3**:
  - 600M parameters
  - More recent, better performance
  - Example: "What is 2+2?" → "4" (correct)

#### Key Insight
- Same architecture, different sizes
- Larger models = more parameters = better performance
- Easy to swap models with same interface

### Dimensions and Shapes

#### Key Hyperparameters
- **Vocabulary Size**: 50,257 (GPT-2)
- **Hidden Dimension**: 768 (GPT-2)
- **Number of Layers**: 12 (GPT-2)
- **Sequence Length**: Variable (up to max)

#### Shape Transformations
- Input IDs: `[batch_size, sequence_length]`
- Embeddings: `[batch_size, sequence_length, hidden_dim]`
- After transformer: `[batch_size, sequence_length, hidden_dim]`
- After LM head: `[batch_size, sequence_length, vocab_size]`
- Last token logits: `[batch_size, vocab_size]`

#### Example Flow
- Input: "hello my name" (3 tokens)
- Embeddings: 3 × 768
- Through transformer: 3 × 768
- LM head output: 3 × 50,257
- Last token: 50,257 (probabilities)

### Key Concepts

#### Parameters vs Hyperparameters
- **Parameters**: Weights in the model (learnable)
  - Example: GPT-2 has 117M parameters
  - Updated during training
- **Hyperparameters**: Design choices (fixed)
  - Example: hidden_dim=768, num_layers=12
  - Set before training

#### Embedding Dimension
- Each token becomes a vector of size hidden_dim
- GPT-2: 768 dimensions
- GPT-3: 12,288 dimensions
- Larger = more capacity but more parameters

#### Sequence Length
- Variable input length
- GPT-2: max 1024 tokens
- Modern models: 4k, 8k, 32k, even millions
- Padding for shorter sequences

### Interactive Playground (Optional)
- UI implementation for testing
- Select model and decoding strategy
- Interactive generation
- More UI code than core logic

### Summary
- Neural networks = sequences of layers
- Linear layers = matrix multiplications
- GPT-2 = decoder-only transformer
- Generation = iterative token prediction
- All LLMs follow similar architecture
- Higher-level libraries abstract these details


