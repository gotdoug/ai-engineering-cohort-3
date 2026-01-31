# Week 3 Agents Guided Learning Part 7 Summary

## MCP Workflow and Tool-Calling Details

### MCP Architecture
- Services (Slack, Google Drive, Zendesk, Gmail, etc.) create MCP servers
- Each service exposes functions as servers; clients connect via protocol
- MCP sits between LLMs and external services; simplifies and standardizes integration

### Using MCP in Practice
1. **Remote MCP servers:** External providers (Slack, Deepgram, Bitbucket) already have servers
2. **Internal databases:** Implement MCP servers for internal DBs; expose as servers
3. **Introduce tools to LLM:** Provide `servers.json` (or similar) listing MCP servers
- Software written once to handle servers config → no code changes when adding tools
- Adding tools = adding entry to config; easy to maintain

### LLM Tool-Calling Training
- LLMs trained on internet data; rarely see function-calling formats
- Companies **fine-tune for function calling** — add data so model learns to output tool calls
- Improves accuracy of when and how to call tools

### Implementation Resources
- Most MCP/tool-calling details already implemented in libraries
- LangChain documentation for tool/function calling
- OpenAI/other providers: specify `model.tools = [add, multiply]`; model becomes aware and can invoke them
