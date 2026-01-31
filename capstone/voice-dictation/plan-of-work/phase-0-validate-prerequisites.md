# Phase 0: Validate Prerequisites (Spike)

Prove that text injection works on macOS before building the full pipeline. Create a minimal app (or script) that:

1. Puts a known string on the clipboard.
2. Simulates Cmd+V via CGEvent (or uses Electron + robotjs/similar).
3. Verifies the text appears in the frontmost app (e.g. TextEdit).

If using Electron (as OpenWhispr does), verify that global shortcuts and paste simulation work. Document exact steps, entitlements, and permission prompts.
