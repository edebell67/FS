# Validation Report: 2026-04-24 Video Package

## Validation Date
2026-04-24T23:55:00Z

## Source Verification

| Claim | Package Value | Source Value | Match |
|-------|---------------|--------------|-------|
| Top Winner Strategy | breakout_Rev_4_tp20.0_sl20.0 | breakout_Rev_4_tp20.0_sl20.0 | YES |
| Top Winner Product | CAD | CAD | YES |
| Top Winner Net | +1215 pips | 1215.0 | YES |
| Worst Loser Strategy | breakout_Rev_2_tp3.0_sl5.0 | breakout_Rev_2_tp3.0_sl5.0 | YES |
| Worst Loser Product | NZDAUD_C | NZDAUD_C | YES |
| Worst Loser Net | -6245 pips | -6245.0 | YES |
| Biggest Reversal | 6195 pips | 6195.0 | YES |
| Positive % | 27% | 27% (795/2898) | YES |
| Negative % | 72% | 72% (2079/2898) | YES |

## Structure Verification

| File | Expected | Present | Valid |
|------|----------|---------|-------|
| summary_net_video_package.json | YES | YES | YES |
| summary_net_video_brief.md | YES | YES | YES |
| summary_net_video_script.txt | YES | YES | YES |
| summary_net_video_storyboard.md | YES | YES | YES |
| summary_net_video_hook_options.txt | YES | YES | YES |
| summary_net_video_overlay_copy.txt | YES | YES | YES |
| summary_net_video_asset_manifest.json | YES | YES | YES |
| summary_net_video_render_notes.md | YES | YES | YES |
| summary_net_video_prompt.txt | YES | YES | YES |
| summary_net_video_thumbnail_brief.txt | YES | YES | YES |
| story_objects.json | YES | YES | YES |

## Narrative Framework Compliance

| Element | Required | Present |
|---------|----------|---------|
| Hook | YES | YES - "CAD leads with +1215 pips" |
| Context | YES | YES - Date, scope, session stats |
| Main Result | YES | YES - Winner description |
| Comparison | YES | YES - Hero vs villain spread |
| Interpretation | YES | YES - Session autopsy |
| Close | YES | YES - CTA included |

## Scope Verification

- [ ] All products are forex-scope: **VERIFIED**
  - CAD: forex
  - NZDAUD_C: forex
- [ ] No off-scope products: **PASSED**

## Quality Checklist

- [x] Claims traceable to _summary_net.json
- [x] Strategy names correct
- [x] Product names correct
- [x] Metrics match source
- [x] Narrative framework followed
- [x] All required files generated
- [x] Package JSON valid
- [x] Story objects serialized correctly

## Comparison to Template

The automated output follows the template structure with:
- Filled placeholders (dates, strategies, products, metrics)
- Proper narrative flow (hook → context → result → comparison → interpretation → close)
- Scene-based storyboard
- Multiple hook options
- Asset manifest for charts

## Result

**VALIDATION PASSED**

All claims verified against source data. Package structure complete. Ready for production use.
