---
name: transcript-summarizer
description: Splits transcript files into ~10-line chunks, generates educational hierarchical bullet summaries for each chunk, then produces a unified final summary. Creates clear, flowing summaries that teach concepts rather than just listing facts. Use when the user wants to summarize a transcript, process office-hour recordings, review-session transcripts, or create structured summaries from long text files.
---

# Transcript Summarizer

Processes long transcript files by chunking, summarizing each chunk with educational hierarchical bullets, then synthesizing a unified final summary. Produces clear, flowing summaries that explain concepts and provide context.

## Workflow

```
Transcript → Split (~10 lines/chunk) → Summarize each chunk (hierarchical bullets) → Unified final summary
```

## Step 1: Split transcript into chunks

Run the split script:

```bash
python .cursor/skills/transcript-summarizer/scripts/split_transcript.py <transcript_path> [--output-dir <dir>] [--chunk-size 10]
```

- **Input**: Path to transcript file (.txt)
- **Output**: Chunk files `transcript-part1.txt`, `transcript-part2.txt`, ... in `--output-dir` (default: same dir as input)
- **Chunk size**: ~10 lines (configurable)

If the script isn't available, split manually: read the file, split by newlines into groups of ~10, write each group to `transcript-partN.txt`.

## Step 2: Summarize each chunk

For each chunk file, create a summary with **hierarchical bullets**:

**Structure:**
- `# Chunk N Summary` (or `# [Source Name] Part N Summary`)
- `##` for major themes/topics
- `###` for subtopics
- `####` for fine-grained points
- Use `-` for bullet items under each heading

**Hierarchical Structure for Education:**
- Use heading levels to organize by concept breadth:
  - `##` = Major themes (e.g., "Diffusion Models")
  - `###` = Key concepts (e.g., "Training Process")
  - `####` = Specific aspects (e.g., "Forward Pass")
- Each level should have a clear parent-child relationship
- Parent bullets state the main concept (1-2 sentences)
- Child bullets add specific details, examples, or implications
- Keep individual bullets concise (1-2 sentences max)
- Use the hierarchy to show relationships:
  - Concept → Details
  - Problem → Solution
  - General → Specific
  - Cause → Effect

**Writing Style:**
- Use complete, flowing sentences that explain concepts clearly
- Provide context: explain WHY things matter, not just WHAT they are
- Assume the reader is learning; define or contextualize technical terms
- Balance brevity with clarity - aim for "succinct but educational"
- Avoid telegraphic shorthand (e.g., "X → Y" or "foo; bar; baz")
- Each bullet should be understandable on its own
- Include key insights, trade-offs, and practical implications

**Guidelines:**
- Capture key ideas, decisions, Q&A, instructions, and takeaways
- Write in complete, clear sentences that flow naturally
- Each bullet should answer: What is this? Why does it matter? How does it work?
- Preserve technical terms, but explain them briefly
- Note transitions between topics

**Output:** Save as `transcript-partN-summary.md` alongside each chunk (or in a `summaries/` subdir).

**Example hierarchy that teaches:**
```markdown
## Diffusion Models

### Training Process
- Diffusion models learn to remove noise from images
  - Forward process: gradually add noise to clean images over steps
  - Backward process: train model to predict and remove the noise
  - Loss function: MSE between predicted and actual noise
  - Key insight: model learns the data distribution through denoising

### Sampling (Generation)
- Start from random noise and iteratively denoise to create images
  - Traditional approach: 1000 denoising steps (slow but high quality)
  - Modern optimizations: DDIM and distillation reduce to 15-20 steps
  - Trade-off: fewer steps mean faster generation but potentially lower quality
```

**Bad vs Good Examples:**

❌ **Bad (Telegraphic):**
```markdown
### VAEs
- Encoder → latent → decoder; MSE loss
- For generation: sample latent, decode
- Not used for generation (blurry); used in diffusion for compression
```

✅ **Good (Educational):**
```markdown
### VAEs (Variational Autoencoders)

#### Architecture
- Two neural networks: encoder and decoder
  - Encoder compresses input images into compact latent representation
  - Decoder reconstructs the original image from this latent code
  - Trained with MSE loss to minimize reconstruction error

#### Generation Process
- Discard encoder and sample random latent codes for generation
  - Pass random samples through decoder to create novel images
  - Main limitation: outputs tend to be blurry and lack fine detail

#### Modern Role
- No longer used for direct image generation due to blurriness
- Critical in diffusion models as compression networks
  - Reduce computational cost by operating in latent space
  - Enable practical video generation (e.g., 512× compression)
```

## Step 3: Unified final summary

Using all chunk summaries, create a **single coherent document** that combines, deduplicates, and merges themes — **without losing any context or details** from the part summaries.

**Approach:**
- **Combine:** Bring all content from part summaries into one document
- **Reduce redundancies:** When the same idea appears in multiple chunks, state it once; consolidate repeated points into a single, complete statement
- **Merge themes:** Group related topics across chunks into unified sections (e.g., all chunking content under one heading, all evaluation content under another)
- **Preserve everything:** Every substantive point, technical term, reference, tool name, command, decision, or instruction from the parts must appear in the final summary — either merged with similar points or as its own bullet
- **No omission:** Do not drop details to shorten; combine and merge instead of cutting

**Structure:**
- `# [Source] Complete Summary`
- High-level overview (2–3 sentences)
- Major sections organized by **theme** (not chunk order)
- Hierarchical bullets within sections
- Cross-reference themes that appear in multiple chunks

**Guidelines:**
- Order by logical flow, not chunk order
- Add a brief "Key takeaways" or "Summary" at top if helpful
- When merging, prefer the more complete or specific wording; include any unique detail from each occurrence
- Verify: every part-summary point has a home in the final document
- Write in clear, educational prose with proper hierarchy
- Use complete sentences; avoid telegraphic bullet points
- Each section should teach the concept, not just list facts
- Explain relationships between concepts (e.g., "VAEs are no longer used for generation, but they're essential in diffusion models for compression")
- Include practical context: why techniques matter, when to use them, trade-offs

**Output:** Save as `[source-name]-complete-summary.md` in the same directory as the transcript or summaries.

## Output locations

| File | Location |
|------|----------|
| Chunks | Same dir as transcript: `transcript-part1.txt`, etc. |
| Chunk summaries | Same dir: `transcript-part1-summary.md`, etc. |
| Final summary | Same dir: `[basename]-complete-summary.md` |

## Quality Checklist

Before finalizing summaries, verify:
- [ ] Each bullet uses complete sentences with clear explanations
- [ ] Technical terms are defined or contextualized on first use
- [ ] The hierarchy is sensical: parent-child relationships are clear
- [ ] The "why" and "how" are explained, not just the "what"
- [ ] A learner could understand the concept from the summary alone
- [ ] No telegraphic shorthand (arrows, semicolons as separators)
- [ ] Concepts are connected (show relationships, not just lists)
- [ ] Key insights, trade-offs, and practical implications are captured
- [ ] Individual bullets are concise (1-2 sentences) but complete
- [ ] The hierarchy does the teaching work: details flow naturally from concepts

## Reference examples

In this repo:
- `project_1/review-session/` — part summaries + `review-session-complete-summary.md`
- `wk2-rag/guided-learning/` — part summaries + `transcript-complete-summary.md` (in transcripts folder)
