# Phase 0: Validate Prerequisites — Text Injection Spike (ExecPlan)

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds.

This document follows PLANS.md and MULTI_AGENT_WORKFLOW_GUIDE.md at the repository root. It implements the spike described in `phase-0-validate-prerequisites.md`.

---

## Purpose / Big Picture

Prove that system-wide text injection works on macOS before building the full voice dictation pipeline. After this spike, you will have a minimal app (or script) that writes a known string to the clipboard and simulates Cmd+V so the text appears in the frontmost application. This validates the core mechanism the voice dictation app will use to inject transcribed text. Success is observable: run the spike, focus TextEdit, trigger the injection, and see "Hello from dictation" appear at the cursor without manually pasting.

---

## Progress

- [ ] Agent 1 (Development): Step 1.1 — Create spike project directory and structure
- [ ] Agent 1 (Development): Step 1.2 — Implement Swift text injection script
- [ ] Agent 1 (Development): Step 1.3 — Add entitlements and build configuration
- [ ] Agent 1 (Development): Step 1.4 — Document exact steps and permission prompts
- [ ] Agent 2 (Verification): Step 2.1 — Run spike and validate in TextEdit
- [ ] Agent 2 (Verification): Step 2.2 — Validate in at least one additional app (e.g., Notes, Slack)
- [ ] Agent 2 (Verification): Step 2.3 — Record outcomes and update Decision Log

---

## Surprises & Discoveries

*(None yet.)*

---

## Decision Log

- **Decision:** Use native Swift for the spike rather than Electron.
  **Rationale:** The macOS implementation plan identifies CGEvent + NSPasteboard as the core mechanism. A Swift script minimizes dependencies and isolates the macOS-specific behavior. Electron can be validated in a later spike if needed.
  **Date/Author:** Initial plan.

- **Decision:** Create a standalone Swift command-line tool or small app bundle.
  **Rationale:** Easiest to run and verify; no need for full Electron setup. Can be invoked from terminal or via a simple launcher.
  **Date/Author:** Initial plan.

---

## Outcomes & Retrospective

*(To be filled when spike completes.)*

---

## Context and Orientation

### Source Documents

- `capstone/voice-dictation/plan-of-work/phase-0-validate-prerequisites.md` — Original spike scope
- `capstone/voice-dictation/voice-dictation-macos-implementation-plan.md` — macOS architecture; text injection research
- `MULTI_AGENT_WORKFLOW_GUIDE.md` — Multi-agent ExecPlan structure

### What We Are Validating

macOS has no public API like Windows TSF for system-wide text injection. The practical approach is: (1) write text to `NSPasteboard`, (2) simulate Cmd+V using `CGEvent` from CoreGraphics. The frontmost app must have focus. This spike proves that sequence works before integrating with audio capture and ASR.

### Key Terms

- **NSPasteboard:** macOS clipboard API. Writing to the general pasteboard makes text available for paste.
- **CGEvent:** CoreGraphics API for creating and posting keyboard/mouse events. Used to simulate Cmd+V.
- **CGEventPost(tap: .cghidEventTap, ...):** Posts events to the HID (human interface device) stream so the system treats them as real keystrokes.
- **Accessibility permission:** Not required for clipboard + simulated paste. Required only if we later add Accessibility API–based injection.

---

## Workflow Orchestration and Agent Coordination

### Initial Trigger (Human Action)

1. Ensure macOS development environment is available (Xcode Command Line Tools or Xcode).
2. Create or confirm the spike directory: `capstone/voice-dictation/plan-of-work/phase-0-spike/`
3. Open TextEdit (or any text editor) and leave it in the foreground with cursor in an empty document.

### Agent Execution Sequence

**Agent 1 (Development) — Steps 1.1–1.4**

- Creates the spike project
- Implements clipboard write + CGEvent Cmd+V simulation in Swift
- Adds entitlements if needed, documents build steps
- Commits to a feature branch (e.g., `feature/phase-0-text-injection-spike`)
- **Checkpoint:** Spike compiles and runs without error; README documents how to run it

**Agent 2 (Verification) — Steps 2.1–2.3**

- Runs the spike with TextEdit focused
- Verifies text appears without manual paste
- Tests in at least one additional app
- Updates Progress, Surprises & Discoveries, Outcomes
- **Checkpoint:** Acceptance criteria met; results documented

### Agent Communication Protocol

- Work is in Git. Development Agent pushes to feature branch; Verification Agent pulls and tests.
- No PR required for this spike unless integrating into main. Checkpoint = branch pushed with working spike.

### Work Tree Management

- Optional: Use `git worktree add /tmp/phase0-spike -b feature/phase-0-text-injection-spike` for isolated work.
- Spike can also be developed in the main work tree; work tree is recommended only if parallel work is happening.

### Error Handling and Recovery

- If CGEvent paste fails: Check that target app has focus; add small delays (`usleep(50000)`) between events.
- If "operation not permitted": Ensure app is not sandboxed, or add `com.apple.security.automation.apple-events` entitlement if automating another app.
- Recovery: Re-run the spike; no persistent state to reset.

---

## Plan of Work

Create a minimal Swift project that:

1. Imports Foundation (for NSPasteboard) and CoreGraphics (for CGEvent)
2. Clears the general pasteboard, writes "Hello from dictation", and declares types for plain text
3. Creates CGEvent objects for Command key down, V key down, V key up, Command key up
4. Sets modifier flags on the V key event so Cmd is held
5. Posts events with brief delays between them
6. Exits

Build as a command-line tool or small app. Provide a README with: how to compile, how to run, what to expect, and any entitlements or permissions required.

---

## Concrete Steps

### Agent 1 (Development)

**Step 1.1 — Create spike project directory and structure**

Working directory: repository root.

    mkdir -p capstone/voice-dictation/plan-of-work/phase-0-spike
    cd capstone/voice-dictation/plan-of-work/phase-0-spike

Create the following structure:

    phase-0-spike/
    ├── main.swift
    ├── README.md
    └── (optional) Package.swift if using Swift Package Manager

**Step 1.2 — Implement Swift text injection script**

Create `main.swift` with the following logic (adapt syntax as needed for your Swift version):

- Get `NSPasteboard.general`
- Call `clearContents()` and `setString("Hello from dictation", forType: .string)`
- Create `CGEventSource(stateID: .combinedSessionState)` (or `privateState`)
- Create events: Command down, V down, V up, Command up using `CGEventCreateKeyboardEvent(source, keyCode, true/false)`
- Key codes: `kVK_Command` (0x37), `kVK_ANSI_V` (0x09)
- On the V key down event, call `CGEventSetFlags(event, .maskCommand)` so Cmd is held
- Post in order: Command down, V down, V up, Command up
- Insert `usleep(50000)` (50ms) between posts for reliability

Expected behavior: When run, the script posts Cmd+V to whatever app is frontmost. User must have TextEdit (or another app) focused before running.

**Step 1.3 — Add entitlements and build configuration**

- If building an app bundle: Create `phase0spike.entitlements` with `com.apple.security.app-sandbox` set to `false` if sandbox blocks automation.
- For a pure CLI tool: Often no entitlements needed. If you see "operation not permitted", add automation entitlement.
- Document the build command, e.g.:

    swiftc -o inject-text main.swift -framework ApplicationServices -framework Foundation

Or use `swift build` if using SPM.

**Step 1.4 — Document exact steps and permission prompts**

In `README.md`, include:

- Prerequisites (Xcode CLI tools or Xcode)
- How to build
- How to run (e.g., `./inject-text`)
- What the user must do first (focus TextEdit, place cursor)
- Expected result: "Hello from dictation" appears at cursor
- Any entitlements or System Settings permissions (e.g., Accessibility) if applicable
- Troubleshooting: "If nothing happens, ensure the target app is frontmost"

**Step 1.5 — Commit and push (checkpoint)**

    git add capstone/voice-dictation/plan-of-work/phase-0-spike/
    git commit -m "Phase 0: Text injection spike for macOS"
    git push origin <branch>

---

### Agent 2 (Verification)

**Step 2.1 — Run spike and validate in TextEdit**

Working directory: `capstone/voice-dictation/plan-of-work/phase-0-spike/`

1. Open TextEdit, create new document, place cursor.
2. Build and run the spike (e.g., `./inject-text`).
3. Observe: "Hello from dictation" must appear at the cursor without manually pressing Cmd+V.

Success: Text appears. Failure: Nothing appears, or wrong app receives paste — document in Surprises & Discoveries.

**Step 2.2 — Validate in at least one additional app**

Repeat with Notes, Slack, or a browser text field. Document which apps work and which do not.

**Step 2.3 — Record outcomes and update Decision Log**

- Update Progress: mark all steps complete.
- If issues found: add to Surprises & Discoveries with evidence.
- Add Outcomes & Retrospective entry summarizing: what worked, what did not, recommendations for the full implementation.

---

## Validation and Acceptance

**Agent 1 completion:** Spike builds and runs. README explains build, run, and expected behavior. Code is committed and pushed.

**Agent 2 completion:** With TextEdit focused, running the spike causes "Hello from dictation" to appear at the cursor. Verified in at least two applications. Outcomes documented.

**Functional acceptance:** A human can run the spike, focus an app, execute the tool, and see the text appear without manual paste. This proves the text injection path is viable for the voice dictation app.

---

## Idempotence and Recovery

- Steps can be repeated. Re-running the spike has no side effects beyond pasting again.
- If the spike directory already exists, overwriting files and rebuilding is safe.
- To start fresh: `rm -rf capstone/voice-dictation/plan-of-work/phase-0-spike` and re-run from Step 1.1.
- Git: Create a new branch if the first attempt is abandoned; work tree can be removed and recreated.

---

## Artifacts and Notes

### Example success transcript

    $ cd capstone/voice-dictation/plan-of-work/phase-0-spike
    $ swiftc -o inject-text main.swift -framework ApplicationServices -framework Foundation
    $ ./inject-text
    (Text "Hello from dictation" appears in focused TextEdit)

### File locations

| File | Path |
|------|------|
| Spike directory | `capstone/voice-dictation/plan-of-work/phase-0-spike/` |
| Main script | `capstone/voice-dictation/plan-of-work/phase-0-spike/main.swift` |
| README | `capstone/voice-dictation/plan-of-work/phase-0-spike/README.md` |

---

## Interfaces and Dependencies

**Frameworks:**

- `Foundation` — NSPasteboard
- `ApplicationServices` (or `CoreGraphics`) — CGEvent, CGEventSource, CGEventPost

**Key APIs:**

- `NSPasteboard.general`
- `NSPasteboard.setString(_:forType:)` with `NSPasteboard.PasteboardType.string`
- `CGEventCreateKeyboardEvent`
- `CGEventSetFlags` with `.maskCommand`
- `CGEventPost(tap: .cghidEventTap, event:)`

**Key codes (from Carbon):**

- `kVK_Command` = 0x37
- `kVK_ANSI_V` = 0x09
