# EP044 Vercel deployment

This folder is a static Vercel-ready site.

## Recommended free-tier setup

1. Push this folder to GitHub as part of the `edebell67/FS` repository.
2. In Vercel, choose **Add New → Project → Import Git Repository**.
3. Select the GitHub repository:

   ```text
   edebell67/FS
   ```

4. Set **Root Directory** to:

   ```text
   epics/ep_044_web_apps/auto-garage-template
   ```

5. Use these settings:

   ```text
   Framework Preset: Other
   Build Command: None / empty
   Output Directory: .
   Install Command: None / empty
   ```

6. Deploy on the Vercel hobby/free tier.

## Local verification

From this folder:

```bash
python3 -m http.server 8097
```

Then open:

```text
http://127.0.0.1:8097/index.html
http://127.0.0.1:8097/owner-preview.html
```

## Notes

- This is a demo template using placeholder content for `Ridgeline Motor Works`.
- Forms and payment-style actions are in demo mode; no real data is sent.
- Before using as a real garage site, personalise `assets/js/config.js`, replace placeholder visuals/content, connect real forms/payments, and switch `demoMode` only after backend verification.
