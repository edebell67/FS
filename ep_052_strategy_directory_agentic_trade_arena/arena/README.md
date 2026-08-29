# Agentic Arena

An interactive 3D JavaScript concept for an autonomous, participant-owned agent portfolio arena.

## Open

Open `index.html` in a modern browser. All code and assets are local; there are no package installs, CDN requests, tracking scripts or API keys.

For a local HTTP preview, run this from this folder:

```powershell
python -m http.server 8052 --bind 127.0.0.1
```

Then visit `http://127.0.0.1:8052`.

The responsive participant portfolio is at `http://127.0.0.1:8052/owner.html`.

To serve the showcase through Uvicorn for another local model or browser client:

```powershell
python -m uvicorn server:app --host 0.0.0.0 --port 8053
```

Open `http://127.0.0.1:8053/` for the Arena or `http://127.0.0.1:8053/owner` for Owner View. A health check is available at `/health`.

## Explore

- Drag the 3D floor to orbit; scroll or use the zoom buttons to move closer. Keyboard arrows orbit; plus/minus zoom.
- Use the expand control for a floor-only presentation; Escape returns to the dashboard.
- Click strategy booths or agent figures to inspect them. The catalogue and rankings provide equivalent accessible buttons.
- Pause/resume, change simulation speed, and switch between balanced, bull, bear and volatile regimes.
- Deploy up to 10 demo agents belonging to the current participant. Agents make their own portfolio decisions.
- Use Owner View to monitor combined and individual performance, allocations, recorded activity, Arena comparisons and shared news on phone or desktop.
- Send owner context or governed commands to pause/resume participation, exit one/all positions, or permanently leave. Owners cannot select purchases, weights or rotations.
- Watch standard/flip purchases, sales, paid intelligence queries, joins, exits and sold-out strategy events.
- Compare best agent returns, descriptive consistency, lowest drawdown and your own agents.
- Switch strategy movers between top and bottom performers.
- Generate a floor report, open a social post or short-video script, copy it or save it as text. There is no external publishing connection.
- Open Arena rules for confirmed rules and explicit demo assumptions.

## What is implemented

The perspective 3D renderer draws actual world-space booth and agent geometry with depth sorting, orbit, elevation and zoom. It uses Canvas 2D as its rasterisation surface, without a third-party 3D library or WebGL dependency.

The deterministic simulation engine records purchases, sales, allocation fees, intelligence fees, cash, units, interest and agent histories. Holdings are valued from unit quantities and current prices. Inventory is conserved. All agents start with exactly one normalised dollar. Rankings use net percentage return.

State is saved in browser local storage. Reloading resumes that state. This is local demo persistence, not a shared or production-grade ledger. The recent event feed is bounded to 240 events and trend charts to 120 samples; totals and all agent identities are retained. Storage can be cleared by the browser and is not cross-device. There is no competition reset button.

## Demo assumptions

- Synthetic agents, strategy prices and intelligence events; no connection to the real Strategy Directory or Trading Engine.
- Each simulation tick advances three hours. The floor starts with 14 simulated days of activity generated through the same ledger.
- Flip units apply the opposite underlying strategy return at each tick, without leverage. Their compounded path is not the simple inverse of the strategy's lifetime return.
- Units use fractional quantities. Returning units on sale makes them available again. This redemption mechanism needs confirmation.
- Exiting agents liquidate, pay exit fees and retain a frozen record. This exit mechanism needs confirmation.
- Cash uses complete 24-hour principal lots and a 365-day year. Credited cash interest does not accrue further interest. An unaffordable intelligence query is not executed or charged.
- “Most consistent” means the fraction of observed steps with non-negative NAV changes. It is descriptive, not a verified skill score; agent ages differ.
- Prices, event feeds and generated content are clearly labelled as simulated. No real money is used.

## Files

- `index.html` — page structure and rules dialogs.
- `owner.html` / `owner.css` / `owner.js` — responsive participant portfolio, metrics, news and governed command interface.
- `styles.css` — responsive interface and reduced-motion styles.
- `engine.js` — deterministic portfolio simulation and state serialization.
- `floor.js` — interactive 3D geometry and animation.
- `app.js` — UI, rankings, inspectors, story drafts and persistence.

## Verification

Run the included tests with Node.js:

```powershell
node --test tests/engine.test.cjs
```

18 tests cover profit/loss haze, engine accounting, bounded long-running prices, persistence, owner messaging, read-only participation, safety exits and permanent leave behavior.

The interface was exercised in the browser for strategy/agent inspection, deployment, rankings, rule dialogs and story generation. Desktop and phone layouts were visually inspected.

Agent haze follows net lifetime return: green above break-even, red below, with stronger haze for larger gains/losses. Break-even has no coloured haze. Booth and action colours remain independent.
