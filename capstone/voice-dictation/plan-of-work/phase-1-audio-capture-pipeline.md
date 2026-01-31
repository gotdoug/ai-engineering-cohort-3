# Phase 1: Audio Capture Pipeline

Implement or reuse a pipeline that:

- Captures microphone input in real time.
- Produces 16 kHz mono, 16-bit chunks.
- Streams or buffers chunks for an ASR backend.

Options: (a) Native Swift/AVAudioEngine, (b) Electron + Node native addon, (c) Electron + separate Python/Node process that receives audio.
