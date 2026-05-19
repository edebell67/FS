# TASK: Fix Mobile Voice Capture (Capacitor Permissions & UI State)

## 1. Problem Description
The mobile app (APK) shows a "mic press" prompt but fails to transition to the recording state (no color change). Voice commands are not being captured on the device.

## 2. Root Cause Analysis
- **Permissions**: Android requires explicit runtime permission for `RECORD_AUDIO`. Standard Web Speech API (used in the current code) often fails or requires specific polyfills/plugins when running inside a native Capacitor wrapper.
- **UI Lifecycle**: The browser-based `SpeechRecognition` might not be triggering the `onstart` event correctly in the mobile context, preventing the color change logic.

## 3. Action Plan
- [ ] **Step 1: Android Manifest Update**
  - Add `<uses-permission android:name="android.permission.RECORD_AUDIO" />` to `AndroidManifest.xml`.
  - Add `<uses-permission android:name="android.permission.MODIFY_AUDIO_SETTINGS" />`.
- [ ] **Step 2: Capacitor Voice Plugin**
  - Install `@capacitor-community/speech-recognition` or `@capacitor/voice-recorder`.
  - Refactor `App.jsx` to use the Capacitor plugin for mobile devices while keeping Web Speech for the desktop.
- [ ] **Step 3: UI State Hardening**
  - Ensure the `isListening` state is tied to the actual hardware activation, not just the button click.
- [ ] **Step 4: Verification**
  - Rebuild APK and test on device.

## 4. Log
- 2026-02-24: Issue reported by user during initial APK test.
