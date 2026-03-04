# Task: Live Market Data - Trading System API Integration

## Status
TODO

## Source
- **Backlog**: `workstream/000_backlog/20260225_104010_live_market_data_pipeline_prompt.md`
- **Phase**: Phase 5 - Storage & Integration
- **Project**: Live Market Data Pipeline

## Description
Provide API endpoint or stream output for real-time algorithmic trading consumption.

## Objective
Enable trading systems to consume live market data via REST API or WebSocket stream.

## Sub-tasks
- [ ] Create `src/api/server.py` with FastAPI:
  ```python
  GET /api/tick/{symbol}      # Latest tick for symbol
  GET /api/ticks              # All latest ticks
  GET /api/health             # System health status
  WS  /ws/stream              # WebSocket price stream
  ```
- [ ] Implement in-memory tick cache:
  - Latest tick per symbol
  - Rolling window of recent ticks
- [ ] Create WebSocket stream:
  - Subscribe to specific symbols
  - Broadcast on new tick
  - Handle client reconnection
- [ ] Add authentication (optional):
  - API key header
  - JWT token
- [ ] Rate limit API endpoints
- [ ] Add Swagger/OpenAPI docs
- [ ] Create client SDK (optional)

## Verification Test
1. `GET /api/tick/BTCUSD` returns latest tick
2. `GET /api/ticks` returns all symbols
3. WebSocket receives ticks in real-time
4. Health endpoint shows provider status
5. Invalid symbol returns 404
6. Rate limit returns 429 after threshold

## Completion Date
(To be filled)
