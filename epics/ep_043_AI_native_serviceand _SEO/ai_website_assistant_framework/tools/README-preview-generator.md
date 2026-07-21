# Private assistant-preview generator

Generate a **private, original shell** for an existing public website and a tenant draft for the shared demo assistant.

```bash
cd C:\Users\edebe\eds\epics\ep_043_AI_native_serviceand _SEO\ai_website_assistant_framework
python tools/create_assistant_preview.py --manifest C:\path\to\prospect.json --output C:\path\to\private_preview
```

## Manifest

```json
{
  "business_name": "Example Motors",
  "source_url": "https://www.example.com/",
  "tenant_key": "auto_example_motors",
  "area": "Bow, London",
  "phone": "+442012345678",
  "services": ["MOT enquiry", "Vehicle service", "Diagnostics"],
  "accent": "#147a78",
  "allowed_origins": ["https://edebell67.github.io"]
}
```

## Generated files

| File | Purpose |
|---|---|
| `capture.json` | Auditable limited public capture: title, meta description, first H1 and navigation labels only |
| `index.html` | Original private concept shell, clearly labelled as not official |
| `assistant-embed.js` | Shared-assistant loader using the generated tenant key |
| `tenant-draft.json` | Demo-safe tenant configuration for review before registry/deploy |

## Deliberate safety boundary

This tool does **not** copy source HTML, CSS, images, reviews, substantial text, or tracking. It does not publish, send outreach, add the tenant to the shared service, or make workflows live.

After review, the tenant draft must be added to `data/clients.json`, tested locally, and deployed to the shared service. The intended preview host must be included in `allowed_origins` before the assistant will load there.
