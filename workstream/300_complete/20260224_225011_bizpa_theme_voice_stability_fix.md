# TASK: Fix Theme Switcher UI & Voice State Instability

## 1. Problem Description
- **UI Vanishing**: Switching to Dark Mode causes the "Upcoming" card to disappear. Switching back to Light Mode does not restore it.
- **Voice Instability**:
  - Mic functionality is tied to the initial theme (works if started in Light, but breaks on switch).
  - Switching themes permanently disables the mic color change/recording state until app restart.
  - Repeated "mic pressed" prompts without transition to active recording.

## 2. Root Cause Analysis
- **UI/DOM Lifecycle**: Theme switching logic might be triggering a React re-render that fails to re-mount the "Upcoming" section or resets its state incorrectly.
- **Microphone Reference Lost**: The `SpeechRecognition` object or its Capacitor plugin equivalent is likely initialized once. Theme switching (which might use a global state update) is likely killing the mic reference or event listeners without re-initializing them.
- **Permissions Latency**: Android permission requests might be clashing with theme-related re-renders.

## 3. Action Plan
- [ ] **Step 1: UI Persistence Fix**
  - Audit `renderDashboard()` and theme-dependent CSS classes for the Upcoming card.
  - Ensure `upcomingItems` state is not cleared during `toggleTheme`.
- [ ] **Step 2: Voice Native Integration**
  - Install `@capacitor-community/speech-recognition`.
  - Move mic initialization to a dedicated `useEffect` that is resilient to theme changes.
  - Implement native permission check before starting the mic.
- [ ] **Step 3: State Sync**
  - Use `useRef` for the Speech object to prevent reference loss during re-renders.
- [ ] **Step 4: Verification**
  - Test starting in Dark vs Light.
  - Test switching modes 3+ times and verify mic still turns red.

## 4. Log
- 2026-02-24: Theme-driven UI/Voice bugs reported during physical device testing.
