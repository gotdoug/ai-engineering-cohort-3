# Week 3 Agents Guided Learning Part 5 Summary

## Tool Calling (Function Calling)

### Why Tools Are Needed
- Workflows still fail for: live data (e.g., weather), calculations, search
- **Tool calling** gives LLMs access to external functions

### Tool-Calling Workflow (Three Steps)
1. **Define the tool:** Write a function (e.g., `add(x, y)` for addition)
2. **Let the LLM know:** Include tool description in system prompt (e.g., special `<tool>` format with name, description, how to use)
3. **Execute when LLM requests:** LLM outputs special token (e.g., `<tool_call>add</tool_call>` with arguments); software parses, calls function, appends result to context, continues generation

### Demo: Add Tool
- System prompt explains: "You can use tool called add; takes number1, number2; returns sum"
- User: "What is X + Y?" → LLM outputs tool call with extracted numbers → software runs `add(X, Y)` → result fed back → LLM produces final answer
- More accurate than LLM doing math internally

### Multiple Tools
- Can add more tools (e.g., weather) to system prompt
- Problem: System prompt becomes long and unwieldy as tools grow
