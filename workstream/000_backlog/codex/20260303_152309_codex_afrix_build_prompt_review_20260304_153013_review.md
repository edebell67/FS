# Build Prompt: AfriX Synthetic African FX Exchange (Frontend)

## Mission
Build a **production-quality frontend** for a synthetic African currency exchange in **under 4 hours of development time**. Speed matters—ship a working product with clean architecture that can be iterated later.

---

## Stack Requirements (Choose ONE, stick with it)

**Option A: Next.js 14+ App Router** (recommended for speed)
- TypeScript required
- Tailwind CSS
- shadcn/ui components
- TradingView Lightweight Charts

**Option B: React + Vite**
- TypeScript required
- Tailwind CSS
- shadcn/ui or headless UI
- TradingView Lightweight Charts

**Common dependencies:**
```json
{
  "lightweight-charts": "^4.1.0",
  "zustand": "^4.4.0",
  "date-fns": "^2.30.0",
  "lucide-react": "latest"
}
```

---

## Core Concept (Read Carefully)

### What This Is
A **synthetic African currency exchange** where users trade tokenized representations of African currencies (sNGN, sKES, sZAR, etc.) against each other. Settlement happens via platform credits ("SETTLE"), NOT via USD/EUR/banks.

### Two Trading Mechanisms (Side-by-Side)
1. **Primary: Order Book Matching**
   - Traditional limit/market orders
   - Central limit order book (CLOB)
   - Price-time priority matching
   
2. **Secondary: DeFi Liquidity Pools**
   - Optional AMM-style pools
   - Users add liquidity to earn fees
   - Can optionally feed passive orders into the order book (UI concept only)

### Critical Rules
- ✅ African currencies ONLY (NGN, KES, ZAR, GHS, EGP, MAD, TZS, UGX, XOF, XAF, etc.)
- ✅ Everything is SYNTHETIC (prefix with 's': sNGN, sKES)
- ✅ NO USD, EUR, GBP anywhere in the app
- ✅ Settlement token is "SETTLE" (not USDT/USDC)
- ✅ Clear "SYNTHETIC" labels throughout UI
- ✅ Pools complement order book, don't replace it

---

## Deliverables Checklist

### Must Have (Core)
- [ ] 5 working pages: Landing, Exchange Terminal, Liquidity, Portfolio, Settings
- [ ] TradingView Lightweight Charts integration with mock data
- [ ] Order book with bid/ask depth visualization
- [ ] Order entry form (limit/market orders)
- [ ] Mock API layer with realistic dummy data
- [ ] Responsive layout (desktop + mobile collapse)
- [ ] TypeScript types for all data models
- [ ] State management (Zustand)
- [ ] README with setup instructions

### Nice to Have (if time permits)
- [ ] WebSocket simulation for live updates
- [ ] Keyboard shortcuts for trading
- [ ] Dark/light theme toggle
- [ ] Advanced order types (stop-loss, take-profit)

---

## Page Specifications

### 1. Landing Page (`/`)
**Purpose:** Convert visitors, explain synthetic model

**Layout:**
```
┌─────────────────────────────────────┐
│  Logo    AfriX    [Enter Exchange]  │
├─────────────────────────────────────┤
│                                     │
│   Trade Synthetic African FX        │
│   First pan-African currency DEX    │
│                                     │
│   [View Markets]  [Add Liquidity]   │
│                                     │
│   ⚠️ Synthetic instruments only     │
│      Not bank settlement            │
│                                     │
│   Featured Markets:                 │
│   sNGN/sKES  sZAR/sGHS  sEGP/sMAD  │
│                                     │
└─────────────────────────────────────┘
```

**Components:**
- Hero section with clear value prop
- Risk disclosure banner (sticky)
- Featured markets grid (3-6 pairs)
- CTA buttons
- Footer with links

---

### 2. Exchange Terminal (`/exchange` or `/trade`)
**Purpose:** Main trading interface

**Desktop Layout (3-column):**
```
┌──────────┬────────────────────┬─────────────┐
│          │                    │ Order Book  │
│ Markets  │   TradingView      │ ────────── │
│ ──────   │      Chart         │ 1.234 (100) │
│ Search   │                    │ 1.233 (250) │
│ ★Favs    │                    │ ────────── │
│          │                    │ 1.232 (180) │
│ sNGN/sKES│   [1D][1W][1M]     │             │
│ sZAR/sGHS│                    │ Recent Trades│
│ sEGP/sMAD│                    │ ────────── │
│          │                    │ 1.233  50   │
│          ├────────────────────┤ 1.234  75   │
│          │ Order Entry        │             │
│          │ [Limit] [Market]   │             │
│          │ [Buy] [Sell]       │             │
│          │ Price: ____        │             │
│          │ Amount: ____       │             │
│          │ [Place Order]      │             │
│          ├────────────────────┤             │
│          │ My Orders | Posns  │             │
└──────────┴────────────────────┴─────────────┘
```

**Mobile Layout (Tabs):**
- Tab 1: Chart
- Tab 2: Order Book
- Tab 3: Trade (Order Entry)
- Tab 4: Orders

**Components Required:**
- `MarketSelector` - searchable list with favorites
- `TradingViewChart` - TradingView Lightweight Charts wrapper
- `OrderBook` - bid/ask depth with grouping
- `RecentTrades` - scrolling trade feed
- `OrderEntry` - form with validation
- `OrderList` - active orders table
- `PositionList` - current positions with PnL

**Mock Behaviors:**
- Market selector switches chart + order book instantly
- Chart updates every 1s with new candle data (random walk)
- Order book updates every 500ms
- Place order → adds to "My Orders" as "Open"
- Cancel order → removes from list

---

### 3. Liquidity Page (`/liquidity`)
**Purpose:** DeFi pool management

**Layout:**
```
┌─────────────────────────────────────┐
│  Liquidity Pools                    │
│  ℹ️ Optional AMM pools - complement │
│     order book, don't replace it    │
├─────────────────────────────────────┤
│  Pool          TVL    APR   Volume  │
│  ─────────────────────────────────  │
│  sNGN/sKES   $1.2M  12.5%   $450K  │
│  sZAR/sGHS   $890K   8.3%   $320K  │
│  sEGP/sMAD   $650K  15.1%   $180K  │
│                                     │
│  [+ Create Pool]                    │
└─────────────────────────────────────┘
```

**Pool Detail Page (`/liquidity/[poolId]`):**
```
┌─────────────────────────────────────┐
│  ← Back    sNGN/sKES Pool           │
├─────────────────────────────────────┤
│  TVL: $1,234,567  APR: 12.5%        │
│  Your Liquidity: $5,000 (0.4%)      │
│  Unclaimed Fees: $12.34             │
├─────────────────────────────────────┤
│  [Add Liquidity] [Remove Liquidity] │
│                                     │
│  Amount sNGN: ____                  │
│  Amount sKES: ____ (balanced)       │
│  You will receive: 123 LP tokens    │
│                                     │
│  □ Also provide to order book       │
│    (experimental market maker mode) │
│                                     │
│  ⚠️ Impermanent loss risk           │
│                                     │
│  [Confirm Add Liquidity]            │
└─────────────────────────────────────┘
```

**Components:**
- `PoolList` - table of all pools
- `PoolCard` - individual pool summary
- `AddLiquidityForm` - dual-input with balance calculation
- `RemoveLiquidityForm` - slider with preview
- `PoolStats` - TVL, volume, fee charts

---

### 4. Portfolio Page (`/portfolio`)
**Purpose:** Account overview

**Layout:**
```
┌─────────────────────────────────────┐
│  Portfolio Value: 125,450 SETTLE    │
├─────────────────────────────────────┤
│  Balances                           │
│  ─────────────────────────────────  │
│  SETTLE    100,000                  │
│  sNGN       12,450                  │
│  sKES        8,320                  │
│  sZAR        4,680                  │
│                                     │
│  Open Positions                     │
│  ─────────────────────────────────  │
│  sNGN/sKES  Long  1000  +$45  +4.5% │
│  sZAR/sGHS  Short  500  -$12  -2.4% │
│                                     │
│  Activity History                   │
│  ─────────────────────────────────  │
│  [Trades] [Orders] [Liquidity]      │
└─────────────────────────────────────┘
```

**Components:**
- `BalanceCard` - total value + breakdown
- `PositionTable` - active positions with PnL
- `ActivityFeed` - filterable history

---

### 5. Settings Page (`/settings`)
**Layout:**
```
┌─────────────────────────────────────┐
│  Settings                           │
├─────────────────────────────────────┤
│  Network                            │
│  ○ Mainnet  ● Testnet               │
│                                     │
│  Display Currency                   │
│  [SETTLE ▼]                         │
│                                     │
│  Confirmations                      │
│  ☑ Confirm large orders (>1000)     │
│  ☑ Warn on high slippage (>2%)      │
│                                     │
│  API Endpoint (Advanced)            │
│  https://api.afrix.exchange         │
│                                     │
│  [Save Settings]                    │
└─────────────────────────────────────┘
```

---

## TypeScript Data Models (Required)

Create `src/types/index.ts` with:

```typescript
export interface Currency {
  code: string;              // "NGN"
  name: string;              // "Nigerian Naira"
  syntheticSymbol: string;   // "sNGN"
  region: string;            // "West Africa"
  decimals: number;          // 2
  flagEmoji?: string;        // "🇳🇬"
}

export interface Market {
  id: string;                // "sNGN_sKES"
  base: Currency;
  quote: Currency;
  symbol: string;            // "sNGN/sKES"
  tickSize: number;          // 0.0001
  minOrderSize: number;      // 10
  makerFee: number;          // 0.001 (0.1%)
  takerFee: number;          // 0.002 (0.2%)
}

export interface OrderBookLevel {
  price: number;
  size: number;
  total?: number;  // cumulative
}

export interface OrderBook {
  market: string;
  bids: OrderBookLevel[];
  asks: OrderBookLevel[];
  spread: number;
  timestamp: number;
}

export interface Trade {
  id: string;
  market: string;
  price: number;
  size: number;
  side: 'buy' | 'sell';
  timestamp: number;
}

export type OrderSide = 'buy' | 'sell';
export type OrderType = 'limit' | 'market';
export type OrderStatus = 'open' | 'filled' | 'cancelled' | 'partial';

export interface Order {
  id: string;
  market: string;
  side: OrderSide;
  type: OrderType;
  price?: number;      // undefined for market orders
  size: number;
  filled: number;
  status: OrderStatus;
  timestamp: number;
  postOnly?: boolean;
}

export interface Position {
  market: string;
  side: 'long' | 'short';
  size: number;
  avgEntryPrice: number;
  currentPrice: number;
  unrealizedPnL: number;
  unrealizedPnLPercent: number;
}

export interface Pool {
  id: string;
  pair: string;            // "sNGN/sKES"
  base: Currency;
  quote: Currency;
  tvl: number;             // in SETTLE
  volume24h: number;
  apr: number;             // 0.125 = 12.5%
  feeTier: number;         // 0.003 = 0.3%
  reserve0: number;
  reserve1: number;
  lpTotalSupply: number;
  price: number;           // reserve1/reserve0
}

export interface Wallet {
  balances: Record<string, number>;  // { "SETTLE": 100000, "sNGN": 12450 }
  totalValue: number;                // in SETTLE
}

export interface CandlestickData {
  time: number;
  open: number;
  high: number;
  low: number;
  close: number;
  volume?: number;
}
```

---

## Mock API Layer

Create `src/lib/api/mock.ts`:

```typescript
import type { Market, OrderBook, Trade, Pool, Wallet } from '@/types';

// Generate realistic mock data
export const mockMarkets: Market[] = [
  {
    id: 'sNGN_sKES',
    symbol: 'sNGN/sKES',
    base: { code: 'NGN', name: 'Nigerian Naira', syntheticSymbol: 'sNGN', region: 'West Africa', decimals: 2 },
    quote: { code: 'KES', name: 'Kenyan Shilling', syntheticSymbol: 'sKES', region: 'East Africa', decimals: 2 },
    tickSize: 0.0001,
    minOrderSize: 10,
    makerFee: 0.001,
    takerFee: 0.002,
  },
  // Add 5-10 more markets
];

export const mockAPI = {
  getMarkets: async (): Promise<Market[]> => {
    await delay(100);
    return mockMarkets;
  },
  
  getOrderBook: async (marketId: string): Promise<OrderBook> => {
    await delay(50);
    return generateMockOrderBook(marketId);
  },
  
  getTrades: async (marketId: string): Promise<Trade[]> => {
    await delay(50);
    return generateMockTrades(marketId);
  },
  
  getPools: async (): Promise<Pool[]> => {
    await delay(100);
    return generateMockPools();
  },
  
  getWallet: async (): Promise<Wallet> => {
    await delay(50);
    return {
      balances: {
        'SETTLE': 100000,
        'sNGN': 12450,
        'sKES': 8320,
        'sZAR': 4680,
      },
      totalValue: 125450,
    };
  },
  
  getCandlestickData: async (marketId: string, interval: string): Promise<CandlestickData[]> => {
    await delay(100);
    return generateMockCandles(marketId, interval);
  },
};

// Helper functions
function delay(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function generateMockOrderBook(marketId: string): OrderBook {
  // Generate realistic bid/ask levels
  const midPrice = 1.234;
  const bids = Array.from({ length: 20 }, (_, i) => ({
    price: midPrice - (i * 0.0001),
    size: Math.random() * 500 + 50,
  }));
  const asks = Array.from({ length: 20 }, (_, i) => ({
    price: midPrice + (i * 0.0001),
    size: Math.random() * 500 + 50,
  }));
  
  return {
    market: marketId,
    bids,
    asks,
    spread: asks[0].price - bids[0].price,
    timestamp: Date.now(),
  };
}

// Add more generator functions...
```

---

## State Management (Zustand)

Create `src/store/useExchangeStore.ts`:

```typescript
import { create } from 'zustand';
import type { Market, Order, Position } from '@/types';

interface ExchangeState {
  selectedMarket: Market | null;
  orders: Order[];
  positions: Position[];
  favorites: string[];
  
  setSelectedMarket: (market: Market) => void;
  addOrder: (order: Order) => void;
  cancelOrder: (orderId: string) => void;
  toggleFavorite: (marketId: string) => void;
}

export const useExchangeStore = create<ExchangeState>((set) => ({
  selectedMarket: null,
  orders: [],
  positions: [],
  favorites: [],
  
  setSelectedMarket: (market) => set({ selectedMarket: market }),
  
  addOrder: (order) => set((state) => ({
    orders: [...state.orders, order],
  })),
  
  cancelOrder: (orderId) => set((state) => ({
    orders: state.orders.map(o => 
      o.id === orderId ? { ...o, status: 'cancelled' as const } : o
    ),
  })),
  
  toggleFavorite: (marketId) => set((state) => ({
    favorites: state.favorites.includes(marketId)
      ? state.favorites.filter(id => id !== marketId)
      : [...state.favorites, marketId],
  })),
}));
```

---

## TradingView Chart Integration

Create `src/components/TradingViewChart.tsx`:

```typescript
import { useEffect, useRef } from 'react';
import { createChart, IChartApi } from 'lightweight-charts';

interface Props {
  data: CandlestickData[];
  height?: number;
}

export function TradingViewChart({ data, height = 400 }: Props) {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);

  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height,
      layout: {
        background: { color: '#ffffff' },
        textColor: '#333',
      },
      grid: {
        vertLines: { color: '#f0f0f0' },
        horzLines: { color: '#f0f0f0' },
      },
    });

    const candlestickSeries = chart.addCandlestickSeries();
    candlestickSeries.setData(data);

    chartRef.current = chart;

    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({ 
          width: chartContainerRef.current.clientWidth 
        });
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  }, [data, height]);

  return <div ref={chartContainerRef} />;
}
```

---

## File Structure

```
afrix-exchange/
├── src/
│   ├── app/                      # Next.js App Router
│   │   ├── layout.tsx
│   │   ├── page.tsx             # Landing
│   │   ├── exchange/
│   │   │   └── page.tsx         # Exchange Terminal
│   │   ├── liquidity/
│   │   │   ├── page.tsx         # Pools List
│   │   │   └── [poolId]/
│   │   │       └── page.tsx     # Pool Detail
│   │   ├── portfolio/
│   │   │   └── page.tsx
│   │   └── settings/
│   │       └── page.tsx
│   │
│   ├── components/
│   │   ├── ui/                  # shadcn/ui components
│   │   ├── MarketSelector.tsx
│   │   ├── TradingViewChart.tsx
│   │   ├── OrderBook.tsx
│   │   ├── OrderEntry.tsx
│   │   ├── OrderList.tsx
│   │   ├── RecentTrades.tsx
│   │   ├── PositionList.tsx
│   │   ├── PoolList.tsx
│   │   ├── PoolCard.tsx
│   │   ├── BalanceCard.tsx
│   │   └── RiskDisclosure.tsx
│   │
│   ├── features/
│   │   ├── exchange/
│   │   │   ├── hooks/
│   │   │   │   ├── useOrderBook.ts
│   │   │   │   ├── useTrades.ts
│   │   │   │   └── useChart.ts
│   │   │   └── utils/
│   │   │       └── orderMatching.ts
│   │   └── liquidity/
│   │       ├── hooks/
│   │       │   └── usePools.ts
│   │       └── utils/
│   │           └── poolMath.ts
│   │
│   ├── lib/
│   │   ├── api/
│   │   │   └── mock.ts          # Mock API layer
│   │   └── utils.ts
│   │
│   ├── store/
│   │   ├── useExchangeStore.ts
│   │   └── useLiquidityStore.ts
│   │
│   ├── types/
│   │   └── index.ts             # All TypeScript types
│   │
│   └── constants/
│       └── currencies.ts        # African currencies list
│
├── public/
│   └── (assets)
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
└── README.md
```

---

## Speed Optimization Tactics

### For Fast Development:
1. **Use shadcn/ui CLI** - Don't build tables/cards from scratch
2. **Copy TradingView examples** - Adapt from their docs
3. **Generate mock data once** - Hardcode 5-10 markets, reuse everywhere
4. **Skip animations initially** - Add polish later
5. **Mobile-first CSS** - Use Tailwind responsive classes, don't overthink layout
6. **Single state store** - Don't split Zustand stores prematurely

### Component Priority:
1. **Build these first:** Layout, MarketSelector, TradingViewChart, OrderEntry
2. **Build these second:** OrderBook, OrderList, PoolList
3. **Build last:** Settings, advanced features

---

## Hard Constraints (MUST FOLLOW)

### Forbidden:
- ❌ No USD, EUR, GBP, or any non-African fiat
- ❌ No mention of "real settlement" or banking integrations
- ❌ No backend code (API routes are mock only)
- ❌ No crypto tokens (BTC, ETH) - this is FX, not crypto
- ❌ No incomplete pages (every route must render)

### Required:
- ✅ "SYNTHETIC" label on every trading screen
- ✅ Risk disclosure on landing page
- ✅ All prices/amounts in SETTLE (settlement token)
- ✅ TradingView Lightweight Charts (not Recharts)
- ✅ TypeScript strict mode
- ✅ Mobile responsive (test at 375px width)
- ✅ Fast market switching (<100ms)

---

## README Requirements

Include in `README.md`:

```markdown
# AfriX - Synthetic African FX Exchange

## Setup
npm install
npm run dev

## Architecture
- Frontend only (mock API)
- State: Zustand
- Charts: TradingView Lightweight Charts
- Components: shadcn/ui

## Mock Data
All data is generated in `src/lib/api/mock.ts`
- Markets: 10 African currency pairs
- Order book updates: every 500ms
- Chart data: random walk simulation

## Future Backend Integration
Replace `mockAPI` calls with real API:
1. Update `src/lib/api/client.ts` with fetch calls
2. Add WebSocket connection in `src/lib/ws.ts`
3. Connect to matching engine at `/api/orders`
4. Connect to pool contracts (EVM or Cosmos)

## Key Features
- Order book trading (limit/market)
- DeFi liquidity pools
- Real-time chart updates
- Portfolio tracking
```

---

## Acceptance Criteria

Before submitting, verify:
- [ ] All 5 pages load without errors
- [ ] TradingView chart renders with mock candle data
- [ ] Can switch markets and chart updates
- [ ] Can place/cancel mock orders
- [ ] Order book shows bid/ask spread
- [ ] Mobile layout works (test in DevTools)
- [ ] No hardcoded USD/EUR anywhere
- [ ] TypeScript compiles with zero errors
- [ ] No console errors on page load

---

## Output Format

Provide:
1. **File tree** (ASCII or markdown list)
2. **Key files** (full code for 10-15 most important files)
3. **README.md** (setup + architecture)
4. **package.json** (with exact dependencies)
5. **One screenshot** (mock terminal view)

---

## Final Notes

**Speed tips:**
- Don't overthink styling—use Tailwind utilities
- Copy component patterns from shadcn examples
- Hardcode mock data, don't generate dynamically yet
- Skip user authentication (add later)
- Commit working code every 30 minutes

**If stuck:**
- TradingView charts: Check `lightweight-charts` npm docs
- Order book: Look at Binance/Coinbase UI for layout
- Pools: Reference Uniswap V2 interface

**Remember:** This is an MVP. Ship fast, iterate later.
\n\n# User Feedback (Task Generation)\nshow details of all tasks\n

## Generated Tasks
| Task | File |
|------|------|
| 20260304_153646_codex_afrix_task_01_from_20260303_152309_codex_afrix_build_prompt_review_20260304_153013 | `050_review/codex/20260304_153646_codex_afrix_task_01_from_20260303_152309_codex_afrix_build_prompt_review_20260304_153013.md` |
| 20260304_153646_codex_afrix_task_02_from_20260303_152309_codex_afrix_build_prompt_review_20260304_153013 | `050_review/codex/20260304_153646_codex_afrix_task_02_from_20260303_152309_codex_afrix_build_prompt_review_20260304_153013.md` |

| Task | File |
|------|------|
| 20260304_153013_codex_afrix_task_01_from_20260303_152309_codex_afrix_build_prompt | `050_review/codex/20260304_153013_codex_afrix_task_01_from_20260303_152309_codex_afrix_build_prompt.md` |
| 20260304_153013_codex_afrix_task_02_from_20260303_152309_codex_afrix_build_prompt | `050_review/codex/20260304_153013_codex_afrix_task_02_from_20260303_152309_codex_afrix_build_prompt.md` |