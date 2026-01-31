# Week 3 Agents Guided Learning Part 2 Summary

## Technical Definition and Levels of Agency

### LLM Capability Demos
- **Simple math:** "3 + 3" → LLM likely correct (seen in training)
- **Complex math:** Large multiplication → LLM may fail; humans use tools (calculator)
- LLMs lack built-in instructions for arithmetic; tools solve this

### AI Agent Definition
- No single universal definition; various definitions share common themes
- **Core properties:**
  - Acts on behalf of users
  - Pursues goals
  - Can **plan**, **reason**, **call tools**, and rely on **memory** to complete complex tasks
- Agent sits between components: coordinates planning, tools, memory; sets up sequence of tasks; returns final response to user

### Levels of Agency
- Agents have different levels of **autonomy**; goal is to give elements more autonomy over time
- **Lowest level:** Single pass (not really an agent)
  - Simple: user prompt → LLM → token generation → stop token → return
  - Low latency, handles only basic prompts
  - LLMs predict next token; software manages the loop (encode → sample → decode)

### Workflows (Next Level)
- **Workflow:** Fixed series of steps; predefined by developer
- No planning involved — the plan is predefined
- Information flows through fixed sequence of steps
- Developer designs predefined code path; orchestration follows it
