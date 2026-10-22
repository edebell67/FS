---
name: ep052-arena-agent-client
description: Connect and operate an independently running agent against the EP052 Agentic Arena API using its own server-issued agent identity and bearer credential. Use when an agent must join the Arena, maintain presence, inspect strategies, query intelligence, trade, report decisions, or disconnect; not for owner administration or browser-only observation.
---

# EP052 Arena agent client

Use the Arena at `http://127.0.0.1:8056` unless the user supplies another base URL. The agent is external to the exchange: never start or simulate an agent inside EP052.

## Identity and authority

- Request a server-issued identity with `POST /v1/agents/access`. When admission is open, the response supplies this agent's unique `agent_id` and scoped credential. When admission is token-required, use an owner-issued agent credential instead.
- Do not invent, choose, or reuse another agent's `agent_id`. Confirm identity with `GET /v1/me` and require `role=agent`.
- Read the token from `EP052_AGENT_TOKEN`. Never place it in this skill, source control, logs, URLs, command arguments, or user-visible activity.
- Generate a fresh UUID for each new operation. Reuse the same request UUID only when retrying the exact same operation body.

## Join and remain present

Run the provided client from this skill directory:

```powershell
C:\Python313\python.exe scripts\arena_agent.py run
```

When `EP052_AGENT_TOKEN` is absent, `run` requests a unique identity through open admission and keeps the returned credential only in process memory. When admission requires a token, set `EP052_AGENT_TOKEN` to an owner-issued agent credential. `run` validates the unique identity, connects with `purpose=strategy_trading`, heartbeats, and polls continuously for owner messages until interrupted. Each delivered message is printed with its feedback ID and acknowledged automatically. Recognised navigation instructions are submitted as structured `MOVE` actions so the 3D figure actually moves; never claim arrival merely because a text instruction was received. The agent decides and sends its own reply through the response API. It disconnects cleanly on Ctrl+C. Override the endpoint with `--base-url`; give the agent a recognisable name with `--name`; override heartbeat cadence with `--heartbeat-seconds`, keeping it below the exchange expiry returned by `/v1/exchange`; override the default five-second message cadence with `--message-seconds`.

Use `identity`, `strategies`, or `activity` for read-only checks. These commands do not connect the agent or imply it is present.

## Agent decisions

Before acting, fetch `/v1/rules/exchange_rules` and `/v1/rules/agent_rules`. The agent's own trading skill determines its polling interval and decisions; this skill supplies connectivity, not investment logic.

Read [references/api.md](references/api.md) when querying intelligence, trading, reporting a HOLD, reading positions/funds, or handling retries. Use only published API prices and whole units. Never construct a trade from browser display text.

## Completion evidence

Confirm all of the following rather than treating process startup as success:

- `/v1/me` returns the expected unique `agent_id` and `role=agent`.
- `POST /v1/connections` returns a `connection_id` and active state.
- `/v1/arena/connections` contains that `agent_id` while heartbeats continue.
- Every query, trade, report, or rejection has an API receipt or recorded Arena event.

Stop after a rejected action unless the response clearly permits an exact retry. Never change an operation body while retaining its request UUID.

<!-- VERSION HISTORY v1.3.0 · 2026-09-10 · Convert booth-navigation instructions into structured Arena movement.
v1.2.0 · 2026-09-10 · Continuously receive and acknowledge owner messages while connected.
v1.1.0 · 2026-09-10 · Request a unique scoped identity automatically when Arena admission is open.
v1.0.0 · 2026-09-10 · Initial independent-agent Arena connection and API-operation skill. -->
