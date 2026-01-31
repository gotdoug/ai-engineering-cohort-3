# Week 3 Agents Guided Learning Part 4 Summary

## Workflow Patterns: Reflection and Parallelization

### Reflection (Evaluator-Optimizer)
- **Problem:** LLM output may be incorrect, incomplete, or suboptimal; previous workflows cannot fix this
- **Solution:** Put generation and evaluation in a loop (feedback loop)
- **Components:** Generator and Evaluator (Critic)
- **Flow:** Generate → Evaluate → Feedback → Regenerate (until satisfied)
- **Evaluator checks:** Factual accuracy, coherence, completeness, adherence to instructions
- **Why separate evaluator:** Same LLM evaluating its own output can be biased; separate model = more robust
- **When to use:** Clear evaluation criteria; known that first attempt may be insufficient
- **Examples:** Code generation (run tests, identify errors); research tasks; creating data plans

### Parallelization
- **Idea:** Run independent steps in parallel instead of sequentially
- **Benefits:** Efficiency (no waiting); robustness (multiple branches can complement each other)
- **Two variations:**
  1. **Sectioning:** Split task into independent subtasks; run in parallel
  2. **Voting:** Same prompt → multiple branches; each solves and generates response; combine/vote on results
- **Voting benefit:** If one branch misses something, another may capture it
- **When to use:**
  - Tasks divisible into subtasks (for speed)
  - Information gathering; multi-API interactions (parallelize slow external calls)
  - Code review for vulnerabilities (multiple branches, each checking different aspects)

### Additional Resources
- Various workflow patterns; workflows vs agents discussion; optimizer patterns
- LangChain code examples for building workflows
