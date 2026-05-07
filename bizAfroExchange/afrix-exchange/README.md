# AfriX - Synthetic African FX Exchange

A production-quality frontend for a synthetic African currency exchange. Trade tokenized African currencies (sNGN, sKES, sZAR, sGHS, etc.) with order book trading and DeFi liquidity pools.

## Setup

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the app.

## Architecture

- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript (strict mode)
- **Styling:** Tailwind CSS
- **Components:** shadcn/ui
- **Charts:** TradingView Lightweight Charts
- **State:** Zustand (with persistence)
- **API:** Mock API layer (frontend only)

## Pages

| Route | Description |
|-------|-------------|
| `/` | Landing page with featured markets |
| `/exchange` | Main trading terminal with chart, order book, order entry |
| `/liquidity` | DeFi pool management |
| `/liquidity/[poolId]` | Individual pool details |
| `/portfolio` | Account balances, positions, history |
| `/settings` | User preferences |

## Mock Data

All data is generated in `src/lib/api/mock.ts`:
- 10 African currency pairs
- Order book updates every 2 seconds
- Chart data with random walk simulation
- 5 liquidity pools

## Key Features

- Order book trading (limit/market orders)
- DeFi liquidity pools with APR
- Real-time chart updates (TradingView)
- Portfolio tracking
- Position management
- Favorites/watchlist

## Trading Pairs

All pairs are synthetic (prefixed with 's'):
- sNGN/sKES (Nigerian Naira / Kenyan Shilling)
- sZAR/sGHS (South African Rand / Ghanaian Cedi)
- sEGP/sMAD (Egyptian Pound / Moroccan Dirham)
- And more...

## Settlement

All trades settle in **SETTLE** tokens (not USD/EUR). This is a synthetic exchange - no real currency settlement.

## Future Backend Integration

Replace `mockAPI` calls with real API:
1. Update `src/lib/api/client.ts` with fetch calls
2. Add WebSocket connection in `src/lib/ws.ts`
3. Connect to matching engine at `/api/orders`
4. Connect to pool contracts (EVM or Cosmos)

## Project Structure

```
src/
├── app/                    # Next.js App Router pages
├── components/             # React components
│   ├── ui/                # shadcn/ui components
│   ├── TradingViewChart.tsx
│   ├── OrderBook.tsx
│   ├── OrderEntry.tsx
│   └── ...
├── store/                  # Zustand stores
├── lib/api/               # Mock API layer
├── types/                 # TypeScript types
└── constants/             # Currencies, markets
```

## License

MIT
