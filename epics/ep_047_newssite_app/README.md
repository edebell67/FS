# EP047 News Site App

Private News-intake service for EP047.

## Purpose

This is the dedicated recipient application for private News JSON batches. It is intentionally separate from the public Directory application:

```text
private/news-intake/*.json
→ validate batch envelope
→ send only validated private batch records to the controlled News import API
→ draft or review_required only
```

It must never publish a story and must not expose intake files over an HTTP route.

## Runtime contract

- Intake: `private/news-intake/*.json`
- Version: `ep047.news-intake/v1`
- Import command: `npm run news:import`
- Required runtime secret: `NEWS_IMPORT_API_URL`
- Required runtime secret: `NEWS_IMPORT_API_KEY`

The credentials are Render environment variables only; do not place them in JSON, source control, logs, or prompts.

## Current state

Local scaffold is created and validates batches. The receiving API and its Render service must be provisioned before production imports can occur.
