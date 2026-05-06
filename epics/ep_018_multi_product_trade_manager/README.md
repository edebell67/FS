# Multi-Product Trade Management Experiment

Runs the same trade-management skill across 2–3 selected products.

Each product gets 3 banking variants by default:

- bank at 25
- bank at 50
- bank at 75

Same price stream. Same rules. Banking threshold is the differentiator.

## Configure products

Edit `config.json`:

```json
"products": ["gbp", "eur"]
```

Use any product code from the API, for example:

```json
"products": ["gbp", "gbpjpy_c"]
```

## Run live

```bash
pip install -r requirements.txt
python trade_manager.py
```

## Logs created

Inside `logs/`:

```text
gbp_price_replay_log.csv
gbp_decision_log.csv
eur_price_replay_log.csv
eur_decision_log.csv
```

## Replay captured prices

```bash
python replay_runner.py
```

## Important

For JPY-style products, pip size is configured as `0.01`.

For most others, pip size defaults to `0.0001`.
