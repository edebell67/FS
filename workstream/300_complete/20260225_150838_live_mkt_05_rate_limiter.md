# Task: Live Market Data - Rate Limit Handler

## Status
TODO

## Source
- **Backlog**: `workstream/000_backlog/20260225_104010_live_market_data_pipeline_prompt.md`
- **Phase**: Phase 2 - Provider Infrastructure
- **Project**: Live Market Data Pipeline

## Description
Implement intelligent rate limiting middleware with adaptive throttling and provider-specific tracking.

## Objective
Prevent API rate limit violations while maximizing data throughput across multiple providers.

## Sub-tasks
- [ ] Create `src/middleware/rate_limiter.py` with:
  ```python
  class RateLimiter:
      def __init__(self, calls_per_minute: int, calls_per_day: int)
      async def acquire(self) -> bool  # wait if needed
      async def try_acquire(self) -> bool  # return False if limited
      def get_wait_time(self) -> float  # seconds until next slot
  ```
- [ ] Implement token bucket algorithm
- [ ] Add provider-specific rate limit tracking
- [ ] Implement exponential backoff on 429 responses:
  - Initial delay: 1s
  - Max delay: 60s
  - Jitter: random 0-500ms
- [ ] Add intelligent caching layer:
  - Cache recent ticks for configurable TTL
  - Return cached if within TTL and rate limited
- [ ] Track rate limit headers from responses
- [ ] Log rate limit events

## Verification Test
1. Set limit to 5 calls/minute
2. Make 10 rapid calls - first 5 succeed, next 5 wait
3. Verify exponential backoff timing
4. Verify cache returns stale data when rate limited
5. Check logs show rate limit events

## Completion Date
(To be filled)
