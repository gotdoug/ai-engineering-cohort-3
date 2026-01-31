# Voice-to-Text Dictation Replication Research

**Capstone idea: replicating a tool like Whisperflow or Willow (AI voice-to-text dictation).**

This document summarizes (1) the current capstone ideas and structure in this directory, and (2) web research on Whisperflow, Willow, and how to replicate such a voice dictation service.

---

## Part 1: Current Capstone Ideas & Structure

### Documents in `capstone/`

| File | Purpose |
|------|--------|
| **capstone-project-ideas.md** | Top replication ideas and “why replication beats generic agents” |
| **research-agent-idea.md** | Research-driven alternative (e.g. cross-pollination engine) |
| **Capstone Project Guidelines - Cohort 3.pdf** | Official cohort guidelines |

### Idea structure (from capstone-project-ideas.md)

- **Strategy**: Prefer **replicas of known products** over vague “multi-agent” or “self-evolving agent” projects so recruiters immediately understand what you built.
- **Top 3 replication options (as of the doc)**:
  1. **Perplexity AI clone** (recommended) — search + reasoning + cited answers; ~5 weeks.
  2. **Sora text-to-video clone** — high wow factor; ~6–7 weeks; more compute.
  3. **NotebookLM clone** — doc Q&A, podcasts, study guides; ~4–5 weeks.
- **Whisperflow** is mentioned in the doc as an example of a replication target (“Maybe a replica of Whisperflow or a replica of Sora”).
- **research-agent-idea.md** argues for a **research cross-pollination engine** (arXiv monitoring, knowledge graph, novel applications) as a more unique but medium-complexity alternative.

### Takeaway

The capstone is framed around either (a) **recognizable product replicas** (Perplexity, Sora, NotebookLM, or **Whisperflow/Willow**) or (b) a **research-driven tool**. Voice dictation fits the “replica of a known product” strategy.

---

## Part 2: What Are Whisperflow and Willow?

### Whisperflow (whisperflow.app / whisperflow.ai)

- **Product**: AI voice dictation app — speech → text with automatic editing (filler removal, habit/typo fixes). “4x faster than typing.”
- **Platforms**: Mac, Windows, iPhone.
- **Features**:
  - Works in any app (Gmail, Slack, Docs, ChatGPT, etc.) without switching.
  - 100+ languages, auto language detection.
  - Personal dictionary, snippet library, voice shortcuts, workflow settings.
- **Pricing** (from research):
  - **Starter**: ~$89/month (basic dictation).
  - **Standard**: ~$169/month (snippets, tones per app, enhanced editing).
  - **Premium**: ~$249/month (team, analytics, custom commands, enterprise security).
  - Free download to start.

*Note: Some search results use “Wispr Flow” / “Wispr Flow”; pricing there was lower (e.g. Pro ~$12–15/user/month). Treat as same product family; confirm on official site.*

### Willow (willowvoice.com / seewillow.com)

- **Product**: AI voice dictation and transcription; “5x faster than typing,” sub-200 ms processing.
- **Platforms**: Mac, Windows, iPhone (50,000+ users cited); app + keyboard for in-app use.
- **Features**:
  - Instant speech-to-text, smart punctuation, auto-formatting.
  - 100+ languages, switchable.
  - Custom dictionary (names, acronyms, products).
  - AI rewrite (tone, grammar, length); style matching (formal/informal by context).
  - Privacy-focused: SOC 2, enterprise security; “never stores voice data” messaging.
- **Pricing**:
  - **Free**: 2,000 words/week (shared across devices).
  - **Individual (Willow Pro)**: ~$15/month (or ~20% off annually); unlimited dictation.
  - **Team**: ~$12/user/month (min 3 seats, annual discount).
  - **Enterprise**: Custom; HIPAA, SSO/SAML, dedicated support.

### Comparison (for replication scope)

| Aspect | Whisperflow | Willow |
|--------|-------------|--------|
| Core | Voice → text + auto-editing | Voice → text + AI rewrite + style |
| Positioning | “4x faster,” universal in-app | “5x faster,” privacy-first |
| Pricing | Higher tiers ($89–249/mo) | Lower entry (Free, ~$12–15/mo) |
| Differentiation | Snippets, tones per app, commands | Style matching, offline, SOC 2 narrative |

Replicating “a Whisperflow or Willow” means: **real-time (or near-real-time) voice → text that can be used across apps**, with optional extras (editing, snippets, style). The **minimum viable replica** is: **streaming speech-to-text + system-wide or in-app text injection**.

---

## Part 3: How to Replicate a Voice Dictation Tool

### 3.1 High-level architecture

1. **Audio capture** — Microphone, chunked stream (e.g. 16 kHz mono, 16-bit).
2. **Speech-to-text** — Streaming ASR (Whisper or similar) via API or local model.
3. **Optional**: Filler-word removal, punctuation, formatting (rule-based or LLM).
4. **Text injection** — Put final (and optionally partial) text where the user is typing: clipboard + paste, or system input injection (accessibility/TSF/keyboard).

### 3.2 Speech-to-text: options (from research)

| Approach | Pros | Cons | Best for |
|--------|------|------|----------|
| **OpenAI Realtime API** | Built-in streaming, low integration effort | Cost, vendor lock-in | Fast prototype, cloud-only |
| **OpenAI Whisper API** | Simple HTTP, no GPU | Per-request latency, not native streaming | Batch or short clips |
| **ufal/whisper_streaming** | Real streaming, local or API backend, ~3.3 s latency | Being superseded by SimulStreaming (2025) | Self-hosted streaming, learning |
| **SimulStreaming** (ufal) | Newer, faster, better quality than whisper_streaming | Newer, fewer backends | Greenfield streaming |
| **Baseten Whisper V3 WebSockets** | Production-style streaming tutorial, WebSocket API | Baseten account/cost | Cloud streaming demo/production |
| **OpenWhispr (open source)** | Full app: hotkey, local/cloud, paste, multi-provider | Desktop-only, no mobile | Capstone “clone” base |
| **WhisperLive / WhisperLiveKit** | Real-time pipeline, WebSocket + FastAPI | You run infra | Self-hosted real-time |
| **Local Whisper (faster-whisper, whisper.cpp, MLX)** | Privacy, no per-minute cost | Need GPU or Apple Silicon, setup | Privacy-first, offline |

Useful references from the repo and web:

- **capstone-project-ideas.md** cites: `github.com/ufal/whisper_streaming` and Baseten’s “Zero to real-time transcription” Whisper V3 WebSockets tutorial.
- **ufal/whisper_streaming**: MIT; supports `faster-whisper`, `whisper_timestamped`, OpenAI API, and MLX; `whisper_online_server.py` for TCP mic streaming; WebSocket + FastAPI via [WhisperLiveKit](https://github.com/QuentinFuxa/WhisperLiveKit).
- **SimulStreaming**: Successor in 2025; better latency/quality; same author; migration path from whisper_streaming.

### 3.3 System-wide “type anywhere” (text injection)

- **Windows**: Text Services Framework (TSF); input injection APIs (e.g. `Windows.UI.Input.Preview.Injection`) to simulate keyboard input system-wide.
- **macOS**: No direct public API like TSF; typically **accessibility APIs** or **synthetic key events**; system dictation is Fn-triggered and not fully programmatic. Third-party apps often use accessibility + paste.
- **Linux**: `xdotool` (X11), `wtype` or `ydotool` (Wayland) to send keys/paste.
- **Mobile**: Custom keyboard (e.g. Willow’s “Dictation & AI Keyboard”) that inserts text into the active field.

**Practical replication**: Desktop = global hotkey → record → transcribe → **copy to clipboard + simulate Ctrl+V**, or use platform input injection where available. OpenWhispr uses this pattern (accessibility on macOS, xdotool/wtype/ydotool on Linux, etc.).

### 3.4 Open-source “clone” base: OpenWhispr

- **Repo**: [OpenWhispr/openwhispr](https://github.com/OpenWhispr/openwhispr) (formerly HeroTools/open-wispr) — ~929+ stars.
- **Stack**: Electron, React 19, TypeScript, Tailwind; Whisper via **whisper.cpp** (local) or OpenAI API (cloud); optional NVIDIA Parakeet (sherpa-onnx); multi-provider AI (OpenAI, Anthropic, Gemini, Groq, local LLM).
- **Features**: Global hotkey, push-to-talk (Windows), auto-paste at cursor, custom dictionary, transcription history (SQLite), cross-platform (Mac/Windows/Linux).
- **Replication strategy**: Fork or use as reference; add/trim features (e.g. “Whisperflow-like” snippets, “Willow-like” style/rewrite) and document your design choices for the capstone.

### 3.5 Tech stack summary for a capstone replica

- **Frontend / desktop**: Electron (or Tauri) for cross-platform app; or web + PWA if you limit to “dictation in browser.”
- **Audio**: Browser `MediaRecorder` / Web Audio or desktop libs (e.g. `sounddevice` in Python); 16 kHz mono, chunked.
- **ASR**: One of:
  - **Cloud**: OpenAI Realtime API, or Whisper API, or Baseten Whisper WebSockets.
  - **Local**: whisper_streaming / SimulStreaming, or OpenWhispr’s whisper.cpp / Parakeet.
- **Streaming**: WebSockets or HTTP streaming; partial + final results for “live” feel.
- **Text output**: Clipboard + simulated paste; or platform input injection (Windows TSF/injection, macOS accessibility, Linux xdotool/wtype/ydotool).
- **Optional**: LLM or rules for filler removal, punctuation, tone; custom dictionary; snippets/shortcuts.

### 3.6 Effort and scope (for capstone)

- **MVP (4–5 weeks)**:  
  - Desktop app (Electron or similar) with hotkey → record → stream to Whisper (API or local) → show transcript + paste (clipboard + Ctrl+V).  
  - One platform (e.g. macOS or Windows) for text injection to reduce integration work.

- **Closer to Whisperflow/Willow (5–6 weeks)**:  
  - Add: custom dictionary, simple “filler word” removal (keyword list or tiny LLM pass).  
  - Optional: snippet expansion (voice shortcut → replace with template).  
  - Optional: “style” or “rewrite” (single LLM call on final segment) to mimic Willow.

- **Stretch**:  
  - Real-time streaming display (partials) like commercial apps.  
  - Second platform (e.g. Windows if you started on Mac).  
  - Or web-only version with WebSocket + Whisper backend.

### 3.7 Portfolio angle

- **One-liner**: “Built a Whisperflow/Willow-style voice-to-text dictation app with real-time streaming, system-wide paste, and optional AI editing.”
- **Technical highlights**: Streaming ASR (Whisper/Realtime API or self-hosted), WebSocket or chunked HTTP pipeline, platform-specific input injection or accessibility, optional LLM post-processing.
- **Differentiation**: Open-source stack, local-first option (privacy), or specific feature (e.g. snippets, style matching) explained and implemented in a minimal but clear way.

---

## Part 4: References (from research)

- Whisperflow: [whisperflow.app](https://whisperflow.app/), [whisperflow.ai](https://whisperflow.ai/).
- Willow: [willowvoice.com](https://willowvoice.com/), [seewillow.com](https://seewillow.com/); [Willow Pricing](https://help.willowvoice.com/en/articles/12854184-willow-pricing-plans-overview).
- ufal/whisper_streaming: [GitHub](https://github.com/ufal/whisper_streaming); paper: “Turning Whisper into Real-Time Transcription System” (IJCNLP-AACL 2023).
- SimulStreaming (successor): [GitHub](https://github.com/ufal/SimulStreaming).
- OpenWhispr: [GitHub](https://github.com/OpenWhispr/openwhispr).
- Baseten: [Zero to real-time transcription: Whisper V3 WebSockets tutorial](https://www.baseten.co/blog/zero-to-real-time-transcription-the-complete-whisper-v3-websockets-tutorial/).
- OpenAI: [Realtime transcription](https://platform.openai.com/docs/guides/realtime-transcription); [Realtime API](https://developers.openai.com/cookbook/examples/realtime_out_of_band_transcription).
- WhisperLiveKit (WebSocket + FastAPI): [GitHub](https://github.com/QuentinFuxa/WhisperLiveKit).
- Windows: [Text Services Framework](https://learn.microsoft.com/en-us/windows/win32/tsf/architecture), [Input injection](https://learn.microsoft.com/en-us/windows/apps/develop/input/input-injection).

---

## Summary

- **Capstone structure**: The repo favors **replicas of known products** (e.g. Perplexity, Sora, NotebookLM); **Whisperflow/Willow** fits that strategy as a recognizable voice dictation product.
- **Whisperflow & Willow**: Both are “speak → polished text everywhere” products; Willow emphasizes privacy and lower price; Whisperflow higher tiers and rich features (snippets, commands).
- **Replication path**: Use **streaming ASR** (OpenAI Realtime, Baseten Whisper WebSockets, or ufal whisper_streaming/SimulStreaming / OpenWhispr) + **text injection** (clipboard + paste or OS input APIs) + optional **editing/snippets/style**. **OpenWhispr** is the strongest open-source base for a desktop “Whisperflow/Willow-like” capstone; you can add or simplify features and document the architecture for the cohort guidelines.
