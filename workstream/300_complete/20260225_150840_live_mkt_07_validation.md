# Task: Live Market Data - Validation Middleware

## Status
TODO

## Source
- **Backlog**: `workstream/000_backlog/20260225_104010_live_market_data_pipeline_prompt.md`
- **Phase**: Phase 3 - Data Quality
- **Project**: Live Market Data Pipeline

## Description
Implement comprehensive data validation layer with configurable thresholds and anomaly detection.

## Objective
Ensure only valid, reliable market data reaches the trading system by filtering out erroneous ticks.

## Sub-tasks
- [ ] Create `src/middleware/validator.py` with:
  ```python
  class TickValidator:
      def __init__(self, config: ValidationConfig)
      async def validate(self, tick: MarketTick) -> ValidationResult
      def is_valid_price(self, price: float) -> bool
      def detect_price_jump(self, tick: MarketTick, previous: MarketTick) -> bool
      def detect_volatility_spike(self, tick: MarketTick, history: List[MarketTick]) -> bool
  ```
- [ ] Implement validation rules:
  - Reject zero prices
  - Reject negative prices
  - Reject NaN/Inf values
  - Detect price jumps > configurable % threshold
  - Detect bid > ask (crossed market)
  - Validate timestamp is recent (< max age)
- [ ] Implement cross-provider validation:
  - Compare tick against secondary provider
  - Flag if deviation > threshold
- [ ] Implement volatility spike detection:
  - Track rolling window of prices
  - Flag if std dev exceeds threshold
- [ ] Log all rejected ticks with reason
- [ ] Expose alert hook for anomalies

## Verification Test
1. Valid tick passes validation
2. Zero price tick is rejected
3. Negative price tick is rejected
4. 50% price jump is flagged (threshold 10%)
5. Crossed market (bid > ask) is rejected
6. Stale timestamp (> 5 min) is rejected
7. Rejected ticks appear in logs with reason

## Completion Date
(To be filled)
