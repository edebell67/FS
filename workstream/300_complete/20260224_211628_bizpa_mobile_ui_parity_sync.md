# TASK: Ensure Mobile/Web UI Parity (Redeploy Assets to APK)

## 1. Problem Description
The user reports that the mobile app UI does not match the current web app (it is likely missing the Milestone 3 updates or has cached older assets).

## 2. Root Cause Analysis
- **Build Sync Gap**: The `npm run build` command might have used a stale `build` folder, or `npx cap sync` did not correctly overwrite the assets in the `android/app/src/main/assets/public` directory.
- **Caching**: The mobile WebView might be caching older versions of `bundle.js`.

## 3. Action Plan
- [ ] **Step 1: Clean Build**
  - Delete `bizPA/frontend/build` directory.
  - Run `npm run build` in `bizPA/frontend`.
- [ ] **Step 2: Force Capacitor Sync**
  - Run `npx cap copy android` followed by `npx cap sync`.
- [ ] **Step 3: Verification**
  - Use `adb shell ls -l /data/data/com.bizpa.app/files` (or similar) to check asset timestamps if possible.
  - Rebuild APK with `gradlew assembleDebug`.
- [ ] **Step 4: Auto-Sync Implementation**
  - Add a script to `package.json` to automate `build + sync + rebuild` to prevent future parity issues.

## 4. Log
- 2026-02-24: User reported mobile UI mismatch.
