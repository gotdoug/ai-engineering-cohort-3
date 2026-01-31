# Voice Dictation Replication — macOS Implementation Overview

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds.

This document follows PLANS.md at the repository root and must be maintained in accordance with it.

---

## Purpose / Big Picture

After this work, you will have a working Whisperflow/Willow-style voice-to-text dictation application for macOS: a desktop app that captures speech via microphone, transcribes it (locally or via API), and injects the resulting text at the cursor in any application. The user presses a global hotkey, speaks, presses again to stop, and the transcribed text appears where they were typing. This is the minimum viable replica: streaming speech-to-text plus system-wide text injection on macOS.

---

## Progress

- [ ] (Draft) Preliminary research completed; plan documented
- [ ] Milestone 0: Validate macOS text injection (proof of concept)
- [ ] Milestone 1: Validate audio capture pipeline
- [ ] Milestone 2: Integrate ASR (Whisper API or local)
- [ ] Milestone 3: End-to-end dictation with hotkey
- [ ] Milestone 4: Polish, packaging, and documentation

---

## Surprises & Discoveries

*(None yet — this is a planning document.)*

---

## Decision Log

- **Decision:** Focus on macOS first for text injection.
  **Rationale:** macOS has no public API like Windows TSF; replication research identifies accessibility + simulated paste as the practical path. Reducing scope to one platform de-risks integration work.
  **Date/Author:** Initial plan.

- **Decision:** Use clipboard + simulated Cmd+V as primary paste mechanism.
  **Rationale:** OpenWhispr and third-party apps use this pattern. Accessibility API alone is unreliable across apps (especially WebKit); combining both methods improves reliability.
  **Date/Author:** Initial plan.

---

## Outcomes & Retrospective

*(To be filled when milestones complete.)*

---

## Context and Orientation

### Source Material

All details below are gathered from:

- `capstone/voice-dictation/voice-dictation-replication-research.md` — Product research (Whisperflow, Willow), architecture, tech stack, effort estimates.
- `capstone/capstone-project-ideas.md` — Replication strategy; Whisperflow mentioned as replication target.
- `PLANS.md` — ExecPlan format and requirements.

### What “Voice Dictation Replication” Means

Replicating Whisperflow or Willow means: real-time (or near-real-time) voice-to-text that works across apps. The minimum viable replica is streaming speech-to-text plus system-wide text injection. Optional extras: filler-word removal, snippets, custom dictionary, AI style/rewrite.

### Key Terms

- **ASR:** Automatic Speech Recognition. Converts audio to text.
- **Text injection:** Putting transcribed text at the user’s cursor in the active application.
- **Accessibility API:** macOS Carbon framework (Application Services) for programmatic control of UI elements; used to assist users with disabilities and, in this context, to inject text.
- **Simulated paste:** Copying text to the clipboard and then programmatically triggering Cmd+V so the frontmost app pastes it.
- **whisper.cpp:** C++ implementation of Whisper; runs locally without Python; used by OpenWhispr.

---

## macOS-Specific Implementation Research

### Text Injection

macOS does not expose a direct, public API like Windows TSF for system-wide text injection. Two approaches are used, often together:

**1. Accessibility API**

- Uses `AXUIElementSetAttributeValue` and related Carbon Accessibility calls.
- Requires: code signing, App Sandbox disabled, and user grant of Accessibility permission (System Settings → Privacy & Security → Accessibility).
- Limitations: WebKit-based apps and some modern text fields use `AXSelectedTextMarkerRange` and `AXTextMarker`, which need extra handling.
- Apps can request permission and monitor changes.

**2. Simulated Paste (Clipboard + Cmd+V)**

- Put text on `NSPasteboard`, then simulate Cmd+V using `CGEvent` from CoreGraphics.
- Use `CGEventCreateKeyboardEvent()` for Command and V, post with `CGEventPost(tap: .cghidEventTap, ...)`.
- The frontmost app must have focus.
- Add small delays (e.g. `usleep(50)`) between events for reliability.

**Practical approach:** Use clipboard + simulated paste as the main path. Add Accessibility-based injection as a fallback or enhancement if needed.

### Audio Capture

- Use **AVAudioEngine** from AVFoundation.
- `engine.inputNode` for microphone; `installTap(onBus: 0, bufferSize: 2048, format: nil)` to process samples in real time.
- Target format: 16 kHz mono, 16-bit (typical for Whisper).
- Requires microphone permission in entitlements and user grant.

### Global Hotkey

- Electron apps (e.g. OpenWhispr) use Electron global shortcuts.
- On macOS, optional Globe/Fn key support uses a bundled Swift helper and requires Xcode Command Line Tools (`xcode-select --install`).
- Native Swift/ObjC apps can use `CGEventTap` or `NSEvent.addGlobalMonitorForEvents`.

### Local Speech-to-Text on macOS

| Option | Notes |
|--------|-------|
| **whisper.cpp** | C++; no Python; bundled in OpenWhispr; GGML models to `~/.cache/openwhispr/whisper-models/` |
| **MLX-Whisper** | Python; uses Apple MLX; ~2x faster than whisper.cpp on Apple Silicon; `pip install mlx-whisper` |
| **sherpa-onnx (Parakeet)** | Alternative local ASR; 25 languages; ~680MB model |
| **OpenAI Whisper API** | Cloud; simple HTTP; not native streaming |
| **OpenAI Realtime API** | Cloud; built-in streaming; higher integration effort |

For a macOS-first, privacy-focused capstone, whisper.cpp or MLX-Whisper are strong local options.

### Permissions Required

- **Microphone:** Required for capture. Declare in entitlements; user must grant in System Settings.
- **Accessibility:** Required if using Accessibility-based paste. User adds app in System Settings → Privacy & Security → Accessibility.
- **App Sandbox:** Disabled if using Accessibility API (common for dictation apps).

---

## Plan of Work

### Phase 0: Validate Prerequisites (Spike)

Prove that text injection works on macOS before building the full pipeline. Create a minimal app (or script) that:

1. Puts a known string on the clipboard.
2. Simulates Cmd+V via CGEvent (or uses Electron + robotjs/similar).
3. Verifies the text appears in the frontmost app (e.g. TextEdit).

If using Electron (as OpenWhispr does), verify that global shortcuts and paste simulation work. Document exact steps, entitlements, and permission prompts.

### Phase 1: Audio Capture Pipeline

Implement or reuse a pipeline that:

- Captures microphone input in real time.
- Produces 16 kHz mono, 16-bit chunks.
- Streams or buffers chunks for an ASR backend.

Options: (a) Native Swift/AVAudioEngine, (b) Electron + Node native addon, (c) Electron + separate Python/Node process that receives audio.

### Phase 2: ASR Integration

Integrate at least one ASR backend:

- **Simplest:** OpenAI Whisper API (non-streaming) for fast prototyping.
- **Streaming:** OpenAI Realtime API, or ufal whisper_streaming / SimulStreaming, or Baseten Whisper WebSockets.
- **Local:** whisper.cpp (via OpenWhispr or similar) or MLX-Whisper.

Deliverable: given audio chunks, obtain transcribed text (partial and/or final).

### Phase 3: End-to-End Dictation

Wire together:

- Global hotkey to start/stop recording.
- Audio capture → ASR → transcribed text.
- Text injection (clipboard + simulated paste, or Accessibility fallback).

User flow: press hotkey → speak → press again → text appears at cursor. Validate in multiple apps (TextEdit, Notes, Slack, browser).

### Phase 4: Polish and Packaging

- Error handling, permission prompts, and clear user instructions.
- Optional: custom dictionary, filler removal, snippets (per replication research).
- Build a distributable macOS app (e.g. .app bundle, optionally DMG); document build and signing if applicable.

---

## Concrete Steps

*(To be expanded as implementation proceeds.)*

**Phase 0 spike (text injection):**

1. Create a minimal Swift or Electron project.
2. Implement clipboard write + Cmd+V simulation.
3. Run with TextEdit in focus; confirm text appears.
4. Document entitlements, sandbox settings, and Accessibility requirements.

---

## Validation and Acceptance

**Phase 0:** After running the spike, pasting “Hello from dictation” into TextEdit (or another app) via simulated Cmd+V succeeds without manual paste.

**End-to-end:** After pressing the hotkey, speaking “The quick brown fox,” and pressing again, the transcribed text appears at the cursor in the active app. Works in at least TextEdit, Notes, and one browser or Slack.

---

## Idempotence and Recovery

- Spike projects can be discarded or kept as reference.
- Prefer additive changes: add new features without breaking existing flows.
- If permissions are revoked, the app should detect and prompt the user to re-grant.

---

## Artifacts and Notes

### References (from research)

- Whisperflow: whisperflow.app, whisperflow.ai
- Willow: willowvoice.com, seewillow.com
- ufal/whisper_streaming: github.com/ufal/whisper_streaming
- SimulStreaming: github.com/ufal/SimulStreaming
- OpenWhispr: github.com/OpenWhispr/openwhispr
- Baseten Whisper WebSockets: baseten.co/blog (real-time transcription tutorial)
- OpenAI Realtime API: platform.openai.com/docs/guides/realtime-transcription

### macOS-Specific References

- Swift/macOS insert text: levelup.gitconnected.com (Accessibility + simulated paste)
- CGEvent paste: Stack Overflow “How to simulate cmd+v event in C/C++ on MacOS”
- AVAudioEngine: developer.apple.com/forums, Stack Overflow “How to get real-time microphone input in macOS”
- MLX-Whisper: github.com/ml-explore/mlx-examples (Whisper), mlx-whisper on PyPI

---

## Interfaces and Dependencies

**Proposed stack (aligns with OpenWhispr and replication research):**

- **Desktop shell:** Electron (or Tauri if minimizing bundle size).
- **Audio:** AVAudioEngine (native) or Node `microphone`/similar via native addon.
- **ASR:** OpenAI Whisper API (start), then whisper.cpp or MLX-Whisper for local.
- **Text injection:** NSPasteboard + CGEvent for Cmd+V; optionally AXUIElement for Accessibility fallback.
- **Hotkey:** Electron `globalShortcut` or native CGEventTap.

**Entitlements (macOS):**

- Microphone usage description.
- Possibly `com.apple.security.automation.apple-events` if automating other apps.
- Sandbox disabled if using Accessibility API.

---

## Effort Estimate (from replication research)

- **MVP (4–5 weeks):** Desktop app with hotkey → record → transcribe → paste. One platform (macOS).
- **Closer to Whisperflow/Willow (5–6 weeks):** Add custom dictionary, filler removal, optional snippets or style/rewrite.

---

## Portfolio Angle

**One-liner:** “Built a Whisperflow/Willow-style voice-to-text dictation app for macOS with real-time transcription, system-wide paste, and optional AI editing.”

**Technical highlights:** Streaming ASR (Whisper/Realtime API or local), platform-specific text injection (clipboard + CGEvent), optional LLM post-processing.
