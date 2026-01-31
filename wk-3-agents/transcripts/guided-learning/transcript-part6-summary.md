# Week 3 Agents Guided Learning Part 6 Summary

## Tool Standardization and MCP

### Scaling Tool Descriptions
- Manually writing tool descriptions in system prompt is **not scalable**
- Need standardization for 100s or 1000s of tools

### Auto-Formatting
- Agree on a format (e.g., function name, arguments, description)
- Extract from function definition → generate textual description
- LLM providers (e.g., Groq) follow same structure → can scale to many tools

### Manual Integration Problem
- Each company writes its own wrapper for external APIs (e.g., Slack)
- Company 1: wrapper for Slack API → integrate into tools
- Company 2: different wrapper, different API — **integration is not standard**
- Automation of tool description helps, but integration remains manual and inconsistent

### MCP (Model Context Protocol)
- Introduced by Anthropic
- **Core idea:** Simplify connecting LLMs to services/tools/databases
- **Approach:** Instead of each company writing wrappers, **service providers** write and expose tools as servers
- Slack (example): creates functions (e.g., `slack_get_channel`), exposes as MCP server
- Companies create MCP client → send requests to MCP server → get responses
- **Benefit:** No need for each company to write wrappers; standard protocol
