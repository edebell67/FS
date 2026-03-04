# TASK: bizPA APK Creation and Deployment Preparation

## 1. Objective
Prepare the bizPA frontend for mobile deployment by setting up a cross-platform wrapper (Capacitor) and generating a production APK.

## 2. Prerequisites
- [ ] Production-ready API URL (replacing `localhost:5055` with a stable cloud or network endpoint).
- [ ] Node.js and NPM installed.
- [ ] Android Studio (with SDK and Build Tools) installed on the build machine.

## 3. Implementation Plan
- [ ] **Phase 1: Environment Hardening**
  - [ ] Abstract `API_BASE_URL` in `App.jsx` to use environment variables (`process.env.REACT_APP_API_URL`).
  - [ ] Implement a fallback mechanism for network-level failures.
- [ ] **Phase 2: Capacitor Integration**
  - [ ] Install Capacitor Core, CLI, and Android: `npm install @capacitor/core @capacitor/cli @capacitor/android`.
  - [ ] Initialize Capacitor: `npx cap init bizPA com.bizpa.app`.
  - [ ] Add Android platform: `npx cap add android`.
- [ ] **Phase 3: Production Build**
  - [ ] Run `npm run build` to generate the `dist` or `build` folder.
  - [ ] Sync assets to Android: `npx cap sync`.
- [ ] **Phase 4: APK Generation**
  - [ ] Open project in Android Studio: `npx cap open android`.
  - [ ] Configure `AndroidManifest.xml` for network permissions (specifically `android:usesCleartextTraffic="true"` if using a non-HTTPS dev API).
  - [ ] Build -> Build Bundle(s) / APK(s) -> Build APK(s).

## 4. Maintenance Notes
- Current Application Version: 1.1.7.
- Build Target: Android API 30+ (Android 11.0+).
