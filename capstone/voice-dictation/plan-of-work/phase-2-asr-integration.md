# Phase 2: ASR Integration

Integrate at least one ASR backend:

- **Simplest:** OpenAI Whisper API (non-streaming) for fast prototyping.
- **Streaming:** OpenAI Realtime API, or ufal whisper_streaming / SimulStreaming, or Baseten Whisper WebSockets.
- **Local:** whisper.cpp (via OpenWhispr or similar) or MLX-Whisper.

Deliverable: given audio chunks, obtain transcribed text (partial and/or final).
