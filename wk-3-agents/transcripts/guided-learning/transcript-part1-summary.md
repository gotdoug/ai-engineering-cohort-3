# Week 3 Agents Guided Learning Part 1 Summary

## Introduction to AI Agents

### What Are Agents?
- Week 3 focuses on **agents**, which are more exciting than previous weeks (prompts, RAG)
- Agents add capability to elements; when you add more capability to elements, you have agents
- Elements (LLMs) lack autonomy: no planning, no performing actions, no breaking complex tasks into subtasks

### LLMs vs Agents: Key Difference
- LLMs are essentially next-token predictors; they struggle with complex, multi-step tasks
- **Example:** "Convince my boss to give me one day off" requires understanding product/market tools, analyzing reports, finding trends, sharing opportunities — too much for an LLM
- Agents are built to address complex prompts and complete tasks on behalf of users

### Real-World Agent Examples
- **Legal agents:** Legal research, drafting
- **Phone agents:** Automate customer phone calls
- **Computer agents:** Access computer and browser (e.g., OpenAI Operator)
- **Codex (ChatGPT):** Agent for software development — synced to repo, has branches/versions; can fix bugs on command
- **Operator:** Uses its own browser — opens browser, searches web, visits websites autonomously
- **Generic agent mode:** Can do anything — search, plan; may take 10–20+ minutes; example: 5-day trip planning with 5 searches, 44 sources

### Technical Goal of Agents
- Make questions answerable
- Smart LLMs know when they cannot answer (e.g., "How's the weather in San Francisco?")
- LLMs need external capabilities (tools) to augment their limitations
- LLMs cannot perform calculations, access live data, or search — they need tool augmentation
