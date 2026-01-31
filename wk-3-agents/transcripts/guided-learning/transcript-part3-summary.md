# Week 3 Agents Guided Learning Part 3 Summary

## Workflow Patterns: Chunking and Routing

### Five Workflow Patterns
- Chunking, Routing, Parallelization, Reflection, and focus/tracking

### Chunking (First Pattern)
- **Problem:** Complex tasks → long context → error propagation
- **Solution:** Decompose into fixed, simpler subtasks
- **Example:** "Analyze topic market, summarize findings" → too much for one LLM call
- Break into: (1) Search for market info, (2) Summarize findings
- Software constructs prompts for each step; chains them sequentially
- **Benefits:** Improved accuracy, easier debugging, clearer error localization

### Routing (Second Pattern)
- **Problem:** Single LLM may not handle different intents or task types well
- **Solution:** Router determines intent of incoming query → directs to specialized branch
- **Three ways to build a router:**
  1. Rule-based (keywords, regex)
  2. ML model (classification)
  3. Semantic routing (similar to RAG) — use embeddings to match to given intents
- **Specialist branches:** Can be LLMs or traditional models (e.g., good at specific tasks)
- **When to use:** Multiple distinct task types; need accurate intent classification
- **Examples:** Customer operations, translation; hard questions → route to most capable model
