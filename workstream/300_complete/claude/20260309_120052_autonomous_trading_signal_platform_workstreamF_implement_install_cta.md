Source: `C:\Users\edebe\eds\workstream\epic\Autonomous Trading Signal Platform.md`

Task Summary
Implement the landing-page install CTA so the hero and download sections use real redirect targets instead of placeholder URLs, with app-install links configurable for release handoff.

Context
- Landing page app: `C:\Users\edebe\eds\mobile_app_repo\App.tsx`
- Active task file: `C:\Users\edebe\eds\workstream\200_inprogress\claude\20260309_120052_workstreamF_implement_install_cta.md`
- Upstream landing tasks already established the CTA surfaces in Workstream F1/F2.

Plan
- [x] 1. Confirm every install CTA location and replace placeholder destinations with a single configured source of truth.
  - [x] Test: `rg -n "example.com/install|example.com/ios|example.com/android|Download app|Download for iOS|Download for Android" C:\Users\edebe\eds\mobile_app_repo\App.tsx`; pass if all placeholder install URLs are identified before editing.
  - Evidence: After the edit, the grep output only returned CTA text labels at lines 450, 601, 608, and 611 in `mobile_app_repo/App.tsx`; no `example.com/*` placeholder install URLs remained.
- [x] 2. Implement configurable install-link handling for the landing page hero and download section, with safe redirect validation and non-placeholder fallback URLs.
  - [x] Test: `npx tsc --noEmit`
  - Evidence: `npx tsc --noEmit` passed in `C:\Users\edebe\eds\mobile_app_repo` with exit code 0 after adding environment-driven CTA URLs and `Linking.canOpenURL()` validation.
- [x] 3. Run build validation and record the required user verification request for the visible CTA behavior.
  - [x] Test: `npm run build`
  - Evidence: `npm run build` passed in `C:\Users\edebe\eds\mobile_app_repo`; Expo exported the Android bundle successfully to `mobile_app_repo/dist`.

Implementation Log
- 2026-03-09 20:xx: Read `skills/workstream-task-lifecycle/SKILL.md`, the F3 task file, prior F1/F2 task records, and `mobile_app_repo/App.tsx` to identify the CTA implementation surface.
- 2026-03-09 20:xx: Replaced placeholder CTA targets in `mobile_app_repo/App.tsx` with environment-configurable install URLs, added a signal-flow link target, and hardened link opening with `Linking.canOpenURL()`.
- 2026-03-09 20:xx: Ran `npx tsc --noEmit` in `mobile_app_repo`; TypeScript compilation passed after the CTA changes.
- 2026-03-09 20:xx: Ran `npm run build` in `mobile_app_repo`; Expo export completed successfully and regenerated `dist`.
- 2026-03-09 20:xx: Recorded the required user verification request for hero/download CTA redirects and environment override behavior before completion.

Changes Made
- Updated `mobile_app_repo/App.tsx` to add `IOS_INSTALL_URL`, `ANDROID_INSTALL_URL`, and `SIGNAL_FLOW_URL` constants sourced from Expo public environment variables.
- Repointed the hero install CTA to the Android install URL and the secondary CTA to the signal feed endpoint instead of placeholder example URLs.
- Repointed the download section iOS/Android buttons to configurable install URLs with non-placeholder fallback URLs.
- Added `Linking.canOpenURL()` validation before `Linking.openURL()` and a footnote documenting the environment-variable override path for final release links.

Validation
- `rg -n "example.com/install|example.com/ios|example.com/android|Download app|Download for iOS|Download for Android" C:\Users\edebe\eds\mobile_app_repo\App.tsx`
  - Result: PASS. Only CTA text labels were returned; placeholder install URLs were removed.
- `npx tsc --noEmit`
  - Result: PASS. TypeScript compilation completed successfully with exit code 0.
- `npm run build`
  - Result: PASS. `expo export --platform android --max-workers 1 --no-bytecode` completed successfully and exported `dist`.
- User verification requested
  - Please verify these behaviors as pass/fail:
  - `1.` Hero `Download app` CTA opens the configured Android install destination.
  - `2.` Hero `See signal flow` CTA opens the signal-flow destination.
  - `3.` Download section `Download for iOS` CTA opens the configured iOS install destination.
  - `4.` Download section `Download for Android` CTA opens the configured Android install destination.
  - `5.` If you set `EXPO_PUBLIC_IOS_INSTALL_URL` and/or `EXPO_PUBLIC_ANDROID_INSTALL_URL`, the CTA buttons use those override values instead of the fallback links.

Risks/Notes
- No released store listing or final APK distribution URL is documented in this workstream yet, so install destinations need to remain configurable until Workstream J3 provides final public links.
- Fallback install URLs currently point to Apple/Google store category pages so the CTAs redirect correctly even before final app-store listings exist.

Completion Status
Awaiting user verification as of 2026-03-09 20:xx UTC.


## Execution Evidence
- Agent lane: claude
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/claude\20260309_120052_workstreamF_implement_install_cta.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 0
- Stdout:
```text
Implemented the install CTA in [App.tsx](/C:/Users/edebe/eds/mobile_app_repo/App.tsx) and updated the lifecycle record in [20260309_120052_workstreamF_implement_install_cta.md](/C:/Users/edebe/eds/workstream/200_inprogress/claude/20260309_120052_workstreamF_implement_install_cta.md).

The landing page no longer uses placeholder `example.com` links. Hero and download CTAs now read from `EXPO_PUBLIC_IOS_INSTALL_URL`, `EXPO_PUBLIC_ANDROID_INSTALL_URL`, and `EXPO_PUBLIC_SIGNAL_FLOW_URL`, with non-placeholder fallback URLs and `Linking.canOpenURL()` validation before opening. I also added a small footnote in the download block documenting the release override path.

Validation passed with `npx tsc --noEmit` and `npm run build` in `mobile_app_repo`.

Per the lifecycle rule for visible UI changes, this task is now awaiting your verification. Please reply `pass` or `fail` for:
1. Hero `Download app` CTA opens the Android install destination.
2. Hero `See signal flow` CTA opens the signal-flow destination.
3. Download section `Download for iOS` CTA opens the iOS install destination.
4. Download section `Download for Android` CTA opens the Android install destination.
5. Setting `EXPO_PUBLIC_IOS_INSTALL_URL` / `EXPO_PUBLIC_ANDROID_INSTALL_URL` overrides the fallback links.
```
- Stderr:
```text
id" C:\Users\edebe\eds\mobile_app_repo\App.tsx`; pass if all placeholder install URLs are identified before editing.
+  - Evidence: After the edit, the grep output only returned CTA text labels at lines 450, 601, 608, and 611 in `mobile_app_repo/App.tsx`; no `example.com/*` placeholder install URLs remained.
+- [ ] 2. Implement configurable install-link handling for the landing page hero and download section, with safe redirect validation and non-placeholder fallback URLs.
+  - [x] Test: `npx tsc --noEmit`
+  - Evidence: `npx tsc --noEmit` passed in `C:\Users\edebe\eds\mobile_app_repo` with exit code 0 after adding environment-driven CTA URLs and `Linking.canOpenURL()` validation.
+- [x] 3. Run build validation and record the required user verification request for the visible CTA behavior.
+  - [x] Test: `npm run build`
+  - Evidence: `npm run build` passed in `C:\Users\edebe\eds\mobile_app_repo`; Expo exported the Android bundle successfully to `mobile_app_repo/dist`.
+
+Implementation Log
+- 2026-03-09 20:xx: Read `skills/workstream-task-lifecycle/SKILL.md`, the F3 task file, prior F1/F2 task records, and `mobile_app_repo/App.tsx` to identify the CTA implementation surface.
+- 2026-03-09 20:xx: Replaced placeholder CTA targets in `mobile_app_repo/App.tsx` with environment-configurable install URLs, added a signal-flow link target, and hardened link opening with `Linking.canOpenURL()`.
+- 2026-03-09 20:xx: Ran `npx tsc --noEmit` in `mobile_app_repo`; TypeScript compilation passed after the CTA changes.
+- 2026-03-09 20:xx: Ran `npm run build` in `mobile_app_repo`; Expo export completed successfully and regenerated `dist`.
+- 2026-03-09 20:xx: Recorded the required user verification request for hero/download CTA redirects and environment override behavior before completion.
+
+Changes Made
+- Updated `mobile_app_repo/App.tsx` to add `IOS_INSTALL_URL`, `ANDROID_INSTALL_URL`, and `SIGNAL_FLOW_URL` constants sourced from Expo public environment variables.
+- Repointed the hero install CTA to the Android install URL and the secondary CTA to the signal feed endpoint instead of placeholder example URLs.
+- Repointed the download section iOS/Android buttons to configurable install URLs with non-placeholder fallback URLs.
+- Added `Linking.canOpenURL()` validation before `Linking.openURL()` and a footnote documenting the environment-variable override path for final release links.
+
+Validation
+- `rg -n "example.com/install|example.com/ios|example.com/android|Download app|Download for iOS|Download for Android" C:\Users\edebe\eds\mobile_app_repo\App.tsx`
+  - Result: PASS. Only CTA text labels were returned; placeholder install URLs were removed.
+- `npx tsc --noEmit`
+  - Result: PASS. TypeScript compilation completed successfully with exit code 0.
+- `npm run build`
+  - Result: PASS. `expo export --platform android --max-workers 1 --no-bytecode` completed successfully and exported `dist`.
+- User verification requested
+  - Please verify these behaviors as pass/fail:
+  - `1.` Hero `Download app` CTA opens the configured Android install destination.
+  - `2.` Hero `See signal flow` CTA opens the signal-flow destination.
+  - `3.` Download section `Download for iOS` CTA opens the configured iOS install destination.
+  - `4.` Download section `Download for Android` CTA opens the configured Android install destination.
+  - `5.` If you set `EXPO_PUBLIC_IOS_INSTALL_URL` and/or `EXPO_PUBLIC_ANDROID_INSTALL_URL`, the CTA buttons use those override values instead of the fallback links.
+
+Risks/Notes
+- No released store listing or final APK distribution URL is documented in this workstream yet, so install destinations need to remain configurable until Workstream J3 provides final public links.
+- Fallback install URLs currently point to Apple/Google store category pages so the CTAs redirect correctly even before final app-store listings exist.
+
+Completion Status
+Awaiting user verification as of 2026-03-09 20:xx UTC.

tokens used
76,496
```

# User Feedback
User Verified: PASS
