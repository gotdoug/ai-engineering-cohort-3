# Week 3 Agents Guided Learning — Complete Summary

This transcript covers AI agents: what they are, how they differ from plain LLMs, levels of agency (single pass → workflows → tool calling → multistep agents), workflow patterns, tool integration (including MCP), multistep and multi-agent systems, and evaluation. The material is from a ByteByteGo guided-learning session.

---

## What Are AI Agents?

### Core Idea
- **Agents** add capability to elements (LLMs). When you give elements more autonomy and tools, you get agents.
- Plain LLMs lack autonomy: they cannot plan, perform actions, or break complex tasks into subtasks.

### LLMs vs Agents
- LLMs are next-token predictors. They struggle with complex, multi-step tasks.
- **Example:** "Convince my boss to give me one day off" requires understanding product/market tools, analyzing reports, finding trends, and sharing opportunities — too much for an LLM.
- Agents are built for complex prompts and can complete tasks on behalf of users.

### Real-World Agent Examples
- **Legal agents:** Legal research, drafting
- **Phone agents:** Automate customer phone calls
- **Computer agents:** Access computer and browser (e.g., OpenAI Operator, Codex)
- **Codex:** Agent for software development — synced to repo, fixes bugs on command
- **Operator:** Uses its own browser to search the web and visit sites
- **Generic agent:** Can plan trips, do research; may take 10–20+ minutes; example: 5-day trip planning with 5 searches, 44 sources

---

## Technical Definition of AI Agents

- No single universal definition; common themes:
  - Acts on behalf of users
  - Pursues goals
  - Can **plan**, **reason**, **call tools**, and use **memory** to complete complex tasks
- The agent sits between components: coordinates planning, tools, and memory; sets up a sequence of tasks; returns the final response.

---

## Levels of Agency

### 1. Single Pass (Lowest — Not Really an Agent)
- Flow: user prompt → LLM → token generation → stop token → return
- Low latency; handles only basic prompts
- LLM predicts next token; software manages encode → sample → decode

### 2. Workflows
- **Fixed series of steps** predefined by the developer
- No planning; the plan is predefined
- Developer designs a predefined code path; orchestration follows it
- Information flows through a fixed sequence

### 3. Tool Calling (Function Calling)
- Gives LLMs access to external functions (calculations, search, live data)
- Workflows alone still fail for: live data (weather), arithmetic, search

### 4. Multistep Agents
- Dynamic workflow instead of fixed
- Agent decides steps based on input and feedback

---

## Workflow Patterns

### Chunking
- **Problem:** Long context and error propagation
- **Solution:** Break complex tasks into fixed subtasks
- Example: "Analyze topic market, summarize findings" → (1) Search market info, (2) Summarize
- Benefits: better accuracy, easier debugging

### Routing
- **Problem:** Single LLM may not handle different intents well
- **Solution:** Router determines intent → directs to a specialized branch
- **Ways to build:** Rule-based, ML classifier, semantic routing (embeddings)
- Specialist branches can be LLMs or traditional models
- Use when: multiple task types, accurate intent classification
- Examples: customer operations, translation; hard questions → most capable model

### Reflection (Evaluator-Optimizer)
- **Problem:** LLM output can be wrong or incomplete; fixed workflows cannot fix it
- **Solution:** Loop: Generate → Evaluate → Feedback → Regenerate
- Components: Generator and Evaluator (Critic)
- Evaluator checks: factual accuracy, coherence, completeness, instruction adherence
- Separate evaluator reduces bias
- Use when: clear evaluation criteria; first attempt often insufficient
- Examples: code generation (run tests), research tasks, data plans

### Parallelization
- **Idea:** Run independent steps in parallel
- **Benefits:** Speed, robustness (multiple branches can complement each other)
- **Variations:**
  - **Sectioning:** Split into subtasks; run in parallel
  - **Voting:** Same prompt → multiple branches → combine/vote on results
- Use when: divisible subtasks, information gathering, multi-API calls, code review for vulnerabilities

---

## Tool Calling (Function Calling)

### Why Tools
- LLMs cannot reliably calculate, access live data, or search without tools.

### Three Steps
1. **Define the tool:** Implement a function (e.g., `add(x, y)`)
2. **Describe to the LLM:** Add tool description to system prompt (e.g., special `<tool>` format with name, args, usage)
3. **Execute:** LLM outputs tool-call token and arguments; software runs the function, appends result to context, continues generation

### Scaling and Standardization
- Manual tool descriptions in prompts do not scale.
- **Auto-formatting:** Standard format (name, args, description) extracted from functions; providers follow same structure so many tools can be exposed.

### Manual Integration Problem
- Each company writes its own wrappers for external APIs (e.g., Slack).
- Integration is inconsistent; automation of descriptions helps, but integration stays manual.

---

## MCP (Model Context Protocol)

- Introduced by Anthropic
- **Idea:** Simplify connecting LLMs to services, tools, and databases
- **Approach:** Service providers (Slack, Google Drive, etc.) implement and expose tools as MCP servers
- Companies create MCP clients → send requests → get responses
- **Benefits:** No per-company wrappers; standard protocol
- **Using MCP:**
  1. Remote MCP servers from external providers
  2. Internal MCP servers for internal DBs
  3. Config file (e.g., `servers.json`) lists servers
- Adding tools = updating config; no code changes in the main app

### LLM Training for Tool Calling
- LLMs rarely see function-calling in pretraining
- Many vendors **fine-tune for function calling** to improve tool use

---

## Multistep Agents

### Workflow Limitations
- Fixed flow; no live information; cannot adapt to input

### Multistep Agent Concept
- Dynamic workflow; agent decides steps
- **Three pillars:** Plan, Act, Adapt
- Agent understands situation and goal → plans → acts → gets feedback → adapts

### Think–Act–Observe Loop
- **Think:** LLM plans next step
- **Act:** Request function call; software runs it and returns output
- **Observe:** Feed output into context; agent reasons and continues
- Loop until task is done

### Planning Strategies
- **ReAct:** Interleaves reasoning and acting (paper, 2023)
- **Reflection:** Natural language feedback from tools
- Others: DFS-style search, various planning methods
- Shared idea: components + loop

---

## Workflows vs Agents

- **Workflows:** Predictable, consistent; good when tasks have clear, fixed paths
- **Agents:** Flexible, autonomous; good when steps are unpredictable or open-ended
- Agents adapt; workflows do not
- Agents can be slower and less reliable (loops, errors)
- Use agents when: open-ended problems; hard to predict steps
- Example: Perplexity Deep Research for structured synthesis

---

## Multi-Agent Systems

- **Motivation:** Single agent may be insufficient
- **Idea:** Multiple agents collaborate; correct/validate each other
- **Architecture:** Manager agent coordinates; uses LLM for planning; activates sub-agents
- **Challenges:** Coordination, communication, compounded errors
- **Protocols:** Agent-to-agent protocols (e.g., Agent2Agent) for discovery and communication; similar role to MCP for tools

---

## Evaluation and Frameworks

### Evaluation Metrics
- **Cost:** More steps → higher cost per request
- **Task success rate:** Benchmarks for specific tasks (e.g., software development)
- Surveys and leaderboards exist (e.g., across banking, insurance, etc.)

### Frameworks
- Many frameworks for building agents (e.g., LangChain, LangGraph)
- LangGraph: used to implement multistep and multi-agent systems
- Implementation with frameworks is often simpler than the theory

---

## Key Takeaways

1. Agents extend LLMs with planning, tools, and memory for complex tasks.
2. Agency scales: single pass → workflows → tool calling → multistep agents.
3. Workflow patterns (chunking, routing, reflection, parallelization) improve fixed workflows.
4. Tool calling gives LLMs access to calculators, search, APIs; MCP standardizes integration.
5. Multistep agents use dynamic think–act–observe loops (e.g., ReAct).
6. Multi-agent systems add coordination and validation; need protocols for communication.
7. Use workflows for predictable tasks; use agents for open-ended, adaptable tasks.
8. Evaluation focuses on cost and task success; frameworks simplify implementation.
