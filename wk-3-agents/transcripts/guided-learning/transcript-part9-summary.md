# Week 3 Agents Guided Learning Part 9 Summary

## Workflows vs Agents, Multi-Agent Systems

### Workflows vs Agents
- **Workflows:** Predictable, consistent; good when tasks have well-defined paths
- **Agents:** Flexible, autonomous; good when steps unpredictable or open-ended
- Agents can adapt to new situations; workflows cannot
- Agents can be slower, less reliable (infinite loops, errors); workflows more stable
- **Use agents when:** Open-ended problems; hard to predict steps ahead of time
- **Example:** Perplexity "Deep Research" — structured information synthesis; detailed reports

### Multi-Agent Systems
- **Motivation:** Single agent may not be capable enough
- **Idea:** Multiple agents collaborate; correct/validate each other → more reliable
- **Architecture:** Manager agent coordinates; has access to LLM for planning; activates sub-agents
- **Challenges:** Coordination, communication, compounded errors

### Protocols for Multi-Agent Communication
- Similar to MCP for tools: need protocol for agents to communicate
- **Agent2Agent protocol:** Defines how agents discover and speak to each other
- Various proposals (MCP, Gateway, etc.); comprehensive discussion in literature
