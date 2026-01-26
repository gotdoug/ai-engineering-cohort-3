# Transcript Part 1 Summary

## Overview
- Introduction to adapting general-purpose LLMs for domain-specific use cases
- Three main techniques: Fine-tuning, Prompt Engineering, and RAG (Retrieval Augmented Generation)

## Why Adaptation is Needed

### General Purpose LLM Use Cases
- Math questions (e.g., "What is two plus two?")
- Brainstorming (e.g., "Help me write an email to my manager")
- Coding questions (e.g., "Fix a bug in my code")
- Works well because model has seen similar examples in training data

### Domain-Specific Use Cases
- Retail store chatbot questions (e.g., "What is your refund policy?")
- Problem: LLM hallucinates or gives incorrect answers
- Example: ChatGPT assumes question is about OpenAI instead of the retail store
- Need: Adapt LLM to use internal documents/knowledge base

### Problem Statement
- Goal: Adapt a general-purpose LLM to accurately answer questions in a specific domain using additional documents
- Documents can be: PDFs, images, HTMLs, Wiki pages, etc.
- Example: Customer asks "What is the refund policy?" → LLM should answer based on document database

## Fine-Tuning

### Concept
- Continue training general-purpose LLM on document database
- Output: Specialized LLM with tuned weights
- Answers come from learned weights (compressed knowledge of training data)

### Two Approaches

#### 1. Updating All Parameters
- Allow optimizer to tune all weights in the LLM
- Problem: Computationally very expensive (billions of parameters)
- Each linear layer's weights are updated

#### 2. Parameter Efficient Fine-Tuning (PEFT)
- Only update a subset of parameters
- Techniques:
  - **Adapters**
    - Freeze original LLM parameters
    - Inject new trainable layers (adapter layers) into transformer architecture
    - Only adapter layers are learned during fine-tuning
    - Paper: "Parameter Efficient Transfer Learning for NLP" (2019)
  - **LoRA (Low-Rank Adaptation)**
    - Freeze original linear layer weights
    - Add two low-rank matrices (A and B) as a parallel branch
    - Output: Wx + ABx (where ABx has same shape as Wx)
    - Only the two new matrices are learnable
    - Advantages over adapters: Faster at inference time
    - Paper: "LoRA: Low-Rank Adaptation of Large Language Models"
  - Other techniques: Prompt tuning, activation scalers, sparse weight deltas

### Practical Implementation
- Library: Hugging Face PEFT
- Example workflow:
  - Load model (e.g., Cohere 2.5B instruct with 3B parameters)
  - Create LoRA config
  - Wrap model with PEFT
  - Result: Only ~0.1% of parameters are trainable (3M out of 3B)
  - Train on dataset
  - Save and load for inference

## Introduction to Prompt Engineering
- Second technique for adapting LLMs
- Preview: Way to craft prompts to extract desired output from LLM

