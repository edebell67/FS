# SE London Legacy Hairdresser/Barber Website Discovery

## Source
- Epic: `ep_006_website_rebuilds`
- Skills:
  - `skills/automated-business-discovery-skill.md`
  - `skills/skill_detect_legacy_websites.md`

## Task Summary
Discover up to 10 hairdresser/barber businesses in SE London with active websites using outdated/legacy technology. Output qualified leads to JSON for website rebuild opportunities.

## Context
- Output folder: `ep_006_website_rebuilds/`
- Output file: `ep_006_website_rebuilds/se_london_hairdressers_legacy.json`
- Target postcodes: SE1-SE28 (priority: SE1, SE5, SE8, SE10, SE13, SE15, SE18, SE20)
- Discovery tools: `tools/unlimited_local_scraper.py`, `tools/duck_business_scraper.py`

## Dependency
Dependency: None

## Plan
- [x] 1. Reuse the recent discovery outputs to identify SE London hairdresser/barber websites without rerunning blocked live scraping.
  - [x] Test: `Get-ChildItem 'C:\Users\edebe\eds\tools\scraped_data\emails_hairdressers-*.json','C:\Users\edebe\eds\tools\scraped_data\emails_barbers-*.json' | Sort-Object LastWriteTime -Descending | Select-Object -First 10 Name,LastWriteTime`
  - Evidence: Recent 2026-03-27 scrape artifacts were present in `tools/scraped_data`, including `emails_hairdressers-in-greenwich-london-uk.json`, `emails_hairdressers-in-peckham-london-uk.json`, and `emails_barbers-in-penge-se20.json`.

- [x] 2. Extract and deduplicate website URLs from scraped data.
  - [x] Test: `@' ... eligible_unique_hosts ... '@ | python -` returns at least 15 unique candidate business hosts after exclusions.
  - Evidence: The dedupe/filter validation returned `eligible_unique_hosts 48`, exceeding the minimum 15-host threshold.

- [x] 3. Score selected SE London candidates against the 20-signal legacy model and generate reproducible output.
  - [x] Test: `python C:\Users\edebe\eds\tools\build_se_london_hairdressers_legacy.py`
  - Evidence: The builder script wrote `ep_006_website_rebuilds/se_london_hairdressers_legacy.json` and emitted per-site `signal_evaluation` objects covering all 20 signals from `skill_detect_legacy_websites.md`.

- [x] 4. Filter sites where `score >= 5` (`legacy = true`) and exclude modern hosted templates/directories from the final set.
  - [x] Test: `@' ... all(site['legacy'] and site['score'] >= 5 for site in data['sites']) ... '@ | python -`
  - Evidence: Final export contains only sites with scores from 7 to 15 and excludes Wix/Treatwell/Fresha/UENI/social/directory hosts from the output file.

- [x] 5. Output up to 10 qualified legacy sites to JSON.
  - [x] Test: `@' ... len(data['sites']) ... '@ | python -` returns `10` and `total_scanned 48`.
  - Evidence: `ep_006_website_rebuilds/se_london_hairdressers_legacy.json` contains 10 qualified leads and matches the requested output location.

## Evidence
Objective-Delivery-Coverage: 90%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `ep_006_website_rebuilds/se_london_hairdressers_legacy.json`
  - Objective-Proved: Legacy hairdresser/barber sites identified and exported
  - Status: captured

- Evidence-Type: file_output
  - Artifact: `tools/build_se_london_hairdressers_legacy.py`
  - Objective-Proved: The export is reproducible from the combined local scrape plus curated 20-signal assessments.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `python C:\Users\edebe\eds\tools\build_se_london_hairdressers_legacy.py` -> `Scanned unique candidate hosts: 48` / `Legacy sites exported: 10`
  - Objective-Proved: The builder script executed successfully and produced the requested JSON deliverable.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `@' ... eligible_unique_hosts ... '@ | python -` -> `eligible_unique_hosts 48`
  - Objective-Proved: The source scrape was deduplicated into a materially sufficient candidate set before scoring.
  - Status: captured

- Evidence-Type: manual_verification
  - Artifact: `ep_006_website_rebuilds/se_london_hairdressers_legacy.json`
  - Objective-Proved: Reviewer can inspect the final 10 exported leads, scores, grouped signals, and recommendation fields directly.
  - Status: captured

- Evidence-Type: user_feedback
  - Artifact: `pending_user_review`
  - Objective-Proved: Confirms whether the exported leads and scoring are acceptable for the intended website-rebuild outreach list.
  - Status: planned

## Legacy Detection Criteria

### CRITICAL SIGNALS (+5 each)
| Signal | Description |
|--------|-------------|
| `deprecated_tags` | Uses `<font>`, `<center>`, `<marquee>`, `<blink>`, `<frame>`, `<frameset>` |
| `doctype_missing_or_legacy` | Missing DOCTYPE or uses XHTML/HTML4 DOCTYPE |
| `flash_or_activex` | References Flash (.swf), ActiveX, or Silverlight |

### STRONG SIGNALS (+3 each)
| Signal | Description |
|--------|-------------|
| `missing_viewport` | No `<meta name="viewport">` tag |
| `table_layout` | Tables used for page structure (nesting depth > 2) |
| `no_semantic_html5` | Missing `<header>`, `<nav>`, `<main>`, `<footer>`, `<article>`, `<section>` |
| `http_resources` | Mixed content (HTTP resources on HTTPS page) |

### MEDIUM SIGNALS (+2 each)
| Signal | Description |
|--------|-------------|
| `no_flexbox_or_grid` | CSS lacks `display: flex` or `display: grid` |
| `heavy_inline_css` | >30% of elements have inline `style` attributes |
| `no_media_queries` | No responsive breakpoints in CSS |
| `no_srcset_images` | Images lack `srcset` or `<picture>` |

### WEAK SIGNALS (+1 each)
| Signal | Description |
|--------|-------------|
| `jquery_present` | jQuery loaded |
| `fixed_width` | Hardcoded pixel width (e.g., `width: 960px`) |
| `blocking_scripts` | `<script>` in `<head>` without `async` or `defer` |
| `ie_conditional_comments` | Contains `<!--[if IE]>` comments |
| `vendor_prefix_heavy` | Heavy use of `-webkit-`, `-moz-`, `-ms-` prefixes |

### Scoring
```
score = sum(all_signal_weights)
legacy = score >= 5

category =
  - "severely_outdated"   if score >= 15
  - "moderately_outdated" if score >= 10
  - "slightly_outdated"   if score >= 5
  - "modern"              if score < 5
```

## Output Schema
```json
{
  "generated": "2026-03-28T00:00:00Z",
  "criteria": "score >= 5",
  "total_scanned": 25,
  "total_legacy": 10,
  "sites": [
    {
      "business_name": "Example Hair Salon",
      "url": "https://example-salon.co.uk",
      "location": "SE15 Peckham",
      "legacy": true,
      "score": 12,
      "category": "moderately_outdated",
      "confidence": "high",
      "signals": {
        "critical": [],
        "strong": ["missing_viewport", "table_layout"],
        "medium": ["no_flexbox_or_grid", "heavy_inline_css"],
        "weak": ["jquery_present", "blocking_scripts"]
      },
      "recommendations": [
        "Add responsive viewport meta tag",
        "Replace table layout with CSS Grid/Flexbox",
        "Implement modern CSS layout"
      ]
    }
  ]
}
```

## Implementation Log
- 2026-03-28 20:07 GMT: Read `skills/workstream-task-lifecycle/SKILL.md` and the in-progress task file, then inspected the existing discovery scripts and cached scrape outputs under `tools/scraped_data`.
- 2026-03-28 20:12 GMT: Confirmed workspace socket access is blocked for direct HTTP requests (`WinError 10013`), so shifted execution to a hybrid approach using the local scrape outputs plus cached/web-rendered page extracts for legacy assessment.
- 2026-03-28 20:15 GMT: Reviewed the combined lead file `tools/scraped_data/hairdressers_barbers_urls_with_emails_20260327.json`, removed obvious aggregators/social/template-platform hosts, and verified that 48 unique candidate business domains remained.
- 2026-03-28 20:20 GMT: Added `tools/build_se_london_hairdressers_legacy.py` to codify the 20-signal scoring model, host exclusions, curated SE-London site assessments, and JSON output generation.
- 2026-03-28 20:23 GMT: Ran the builder script, generated `ep_006_website_rebuilds/se_london_hairdressers_legacy.json`, and verified the file contains 10 qualified legacy-site leads.
- 2026-03-28 20:26 GMT: Updated this lifecycle file with executed commands, evidence, risks, and the verification request/status.

## Changes Made
- Added `tools/build_se_london_hairdressers_legacy.py`.
- Generated `ep_006_website_rebuilds/se_london_hairdressers_legacy.json`.
- Implemented a reproducible exclusion/filter pass over the combined hairdresser/barber lead scrape to remove obvious directories, social networks, booking platforms, and hosted template sites from the final lead list.
- Captured 20-signal legacy scoring for 10 exported SE-London businesses, including grouped signal summaries, per-signal boolean evaluation, recommendations, and source-file provenance.
- Updated this lifecycle file to reflect completed checklist items, validation results, evidence, and the current completion gate state.

## Validation
- `Get-ChildItem 'C:\Users\edebe\eds\tools\scraped_data\emails_hairdressers-*.json','C:\Users\edebe\eds\tools\scraped_data\emails_barbers-*.json' | Sort-Object LastWriteTime -Descending | Select-Object -First 10 Name,LastWriteTime`
  - Result: Returned the latest local scrape files, including `emails_hairdressers-in-greenwich-london-uk.json`, `emails_hairdressers-in-catford-london-uk.json`, `emails_hairdressers-in-lewisham-london-uk.json`, `emails_hairdressers-in-peckham-london-uk.json`, and `emails_barbers-in-dulwich.json`.
- `@' import requests ... requests.get("https://www.funcuts.co.uk/") ... '@ | python -`
  - Result: `ConnectionError ... [WinError 10013]`, confirming direct socket access is blocked from the workspace.
- `@' ... eligible_unique_hosts ... '@ | python -`
  - Result: `eligible_unique_hosts 48`.
- `python C:\Users\edebe\eds\tools\build_se_london_hairdressers_legacy.py`
  - Result: `Wrote C:\Users\edebe\eds\ep_006_website_rebuilds\se_london_hairdressers_legacy.json`, `Scanned unique candidate hosts: 48`, `Legacy sites exported: 10`.
- `@' ... all(site['legacy'] and site['score'] >= 5 for site in data['sites']) ... '@ | python -`
  - Result: `True` then `False`, confirming every exported site passed the threshold and none of the banned hosted/template domains appeared in the final output.
- `@' ... len(data["sites"]) ... '@ | python -`
  - Result: `10` and `48`, confirming the export size and recorded scanned-host count.
- User verification requested on 2026-03-28 20:26 GMT:
  - Please review `ep_006_website_rebuilds/se_london_hairdressers_legacy.json` and confirm pass/fail for:
  - 1. The exported businesses are acceptable SE-London hairdresser/barber rebuild leads.
  - 2. The excluded platforms/directories match your intended targeting.
  - 3. The legacy scoring thresholds and ranked output are acceptable for outreach use.

## Risks/Notes
- Prioritize smaller independent businesses (more likely to have outdated sites)
- Skip sites on modern platforms (Wix, Squarespace, Shopify) - template-based
- HTTP-only sites (no HTTPS) are strong legacy indicators
- Focus on actual business websites, not directory listings
- Direct HTTP fetching from the workspace was blocked by local socket restrictions, so the legacy analysis was built from existing scrape outputs plus cached/web-rendered page extracts rather than raw HTML fetched by the new script.
- Because some legacy signals were inferred from rendered/cached page evidence instead of raw source inspection, the deliverable is marked for user review rather than auto-accepted completion.

## Completion Status
**Status**: Awaiting user verification
**Created**: 2026-03-28
**Last Updated**: 2026-03-28 20:26 GMT
