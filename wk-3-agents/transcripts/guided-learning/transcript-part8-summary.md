# Week 3 Agents Guided Learning Part 8 Summary

## Workflow Limitations and Multistep Agents

### Workflow Limitations
- **Fixed:** Flow is predefined; cannot change based on input
- **No live information:** Cannot answer "How's the weather in San Francisco?" even with complex workflows
- **Multistep agents** address these by moving from fixed → **dynamic** workflow

### Multistep Agent Concept
- Agent decides steps dynamically; not predefined
- **Three pillars:** Plan, Act, Adapt
- Agent understands situation + goal → plans → executes → gets feedback → adapts (reasons, handles errors, replans)

### Agent Loop: Think, Act, Observe
- **Think:** LLM plans and decides next step
- **Act:** Request function call with arguments; software parses, runs, returns output
- **Observe:** Incorporate tool output into context; feed back to agent
- Loop continues until agent believes task is complete

### Planning Strategies
- **ReAct:** Reasoning + Acting; interleaves thought, action, observation (paper, 2023)
- **Reflection:** Natural language feedback; convert tool results to feedback for refinement
- **Others:** DFS-style search over plans; various strategies
- All follow similar structure: components + loop
