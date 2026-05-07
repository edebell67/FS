# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Development
npm run dev              # Start dev server (default: localhost:3000)
npm run build            # Production build
npm start                # Start production server
npm run lint             # ESLint check

# Testing
npm test                 # Run all tests
npm run test:watch       # Watch mode
npm run test:coverage    # With coverage report
npx jest __tests__/components.test.tsx  # Run single test file
```

## Architecture

### Server/Client Component Separation
This Next.js 14 App Router project strictly separates server and client code:

- **`src/app/page.tsx`** (Server) - Fetches data using Node.js `fs` module, passes to client
- **`src/app/ClientPage.tsx`** (Client) - All interactive UI with `'use client'` directive
- **`src/lib/data.ts`** (Server only) - Data fetching with `fs.readFile()` - cannot be imported in client components
- **`src/lib/data-client.ts`** (Client safe) - Pure functions duplicated for client-side use: `filterStrategies()`, `calculateDashboardMetrics()`, `getSignificantMovers()`

### Data Flow
1. Server component reads JSON files from `DATA_BASE_PATH` in `src/lib/data.ts`
2. Data passed as props to `ClientPage`
3. Client-side filtering/calculations use functions from `data-client.ts`
4. API routes (`/api/strategies`, `/api/strategies/[strategy]`) provide data for dynamic requests

### State Management
Zustand store at `src/hooks/useStore.ts` manages:
- Filter state (strategy, product, net range, pickNowOnly)
- Selected strategy for detail view
- Authentication state and gating
- Modal visibility

### Data Source
Reads `_top20.json` and `_summary_net.json` from:
```
/mnt/c/Users/edebe/eds/TradeApps/breakout/fs/json/live/forex/{date}/
```
Path configured in `src/lib/data.ts` as `DATA_BASE_PATH`.

## Key Types

Defined in `src/types/index.ts`:
- `TopStrategy` - Individual strategy with net P&L, win rates, pick status
- `Top20Data` - Container with `last_update` and `top20` array
- `SummaryNetData` - Time-series data nested by strategy > product > entries
- `FilterState` - Current filter configuration
- `DashboardMetrics` - Aggregated metrics for display

## Path Alias

Uses `@/*` alias mapped to `./src/*` (configured in `tsconfig.json`).

## Testing

Jest with React Testing Library. Setup in `jest.setup.js`. Tests in `__tests__/` directory.
Components require mocking Zustand store when testing interactive elements.
