# Task: Live Market Data - Configuration System

## Status
TODO

## Source
- **Backlog**: `workstream/000_backlog/20260225_104010_live_market_data_pipeline_prompt.md`
- **Phase**: Phase 1 - Foundation
- **Project**: Live Market Data Pipeline

## Description
Implement a flexible YAML-based configuration system that supports all configurable parameters without hardcoded values.

## Objective
Enable runtime configuration of symbols, providers, thresholds, polling frequencies, and output modes via external config file.

## Sub-tasks
- [ ] Create `config/config.yaml` with sections:
  - providers (list with credentials placeholder)
  - symbols (per asset class)
  - validation (thresholds)
  - polling (frequencies)
  - storage (output mode)
  - logging (level, format)
- [ ] Create `src/utils/config_loader.py`:
  - Load YAML config
  - Environment variable substitution for secrets
  - Validation of required fields
  - Default value handling
- [ ] Create Pydantic models for config validation:
  - `ProviderConfig`
  - `SymbolConfig`
  - `ValidationConfig`
  - `StorageConfig`
- [ ] Support config reload without restart (optional)

## Verification Test
1. Create sample `config.yaml` with all sections
2. Run config loader - should parse without errors
3. Missing required field should raise clear error
4. Environment variable `${API_KEY}` should be substituted
5. Invalid threshold value should be rejected by Pydantic

## Completion Date
(To be filled)
