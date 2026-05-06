# Strategy Performance View

A modern, mobile-friendly web dashboard for monitoring top trading strategy performance with real-time analytics.

## Features

- **Dashboard Overview**: High-level metrics including total P&L, strategy count, win rates, and active picks
- **Top 20 Strategies**: Sortable table with filtering by strategy, product, net range, and active status
- **Significant Movers**: Highlights top gainers and losers for quick insight
- **Product Breakdown**: Visual chart showing performance by product type
- **Strategy Details**: Drill-down view with daily/weekly performance charts
- **Authentication**: Sign-in/sign-up modals for gated content access
- **Responsive Design**: 100% mobile-friendly with touch-optimized interactions

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Charts**: Recharts
- **State Management**: Zustand
- **Testing**: Jest + React Testing Library

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

```bash
# Navigate to project directory
cd ep_010_strategy_performance_view

# Install dependencies
npm install

# Run development server
npm run dev
```

The application will be available at `http://localhost:3000`

### Build for Production

```bash
# Build the application
npm run build

# Start production server
npm start
```

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

## Project Structure

```
ep_010_strategy_performance_view/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── api/            # API routes
│   │   ├── page.tsx        # Main page (server component)
│   │   ├── ClientPage.tsx  # Client-side interactive page
│   │   ├── layout.tsx      # Root layout
│   │   └── globals.css     # Global styles
│   ├── components/         # React components
│   │   ├── Navigation.tsx
│   │   ├── AuthModal.tsx
│   │   ├── Dashboard.tsx
│   │   ├── MetricCard.tsx
│   │   ├── FilterPanel.tsx
│   │   ├── StrategiesTable.tsx
│   │   ├── StrategyDetail.tsx
│   │   ├── SignificantMovers.tsx
│   │   └── PerformanceChart.tsx
│   ├── hooks/              # Custom React hooks
│   │   └── useStore.ts     # Zustand store
│   ├── lib/                # Utility functions
│   │   ├── data.ts         # Data fetching & processing
│   │   └── utils.ts        # Helper functions
│   └── types/              # TypeScript types
│       └── index.ts
├── __tests__/              # Test files
├── public/                 # Static assets
├── package.json
├── tailwind.config.ts
├── tsconfig.json
└── README.md
```

## Data Sources

The application reads data from:
- `_top20.json` - Top 20 performing strategies
- `_summary_net.json` - Detailed time-series data for each strategy

Data path: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\{date}\`

## Design System

Following the web-design-guidelines skill with:
- Clean, editorial-style interface
- Warm monochrome palette with emerald/rose accents
- Premium typography (Geist font family)
- Subtle animations and micro-interactions
- Mobile-first responsive design
- No emojis, no AI copywriting cliches

## API Routes

### GET /api/strategies
Returns filtered strategy data with dashboard metrics.

Query parameters:
- `date` - Date string (default: 2026-04-03)
- `strategy` - Strategy name filter
- `product` - Product filter
- `minNet` - Minimum net P&L
- `maxNet` - Maximum net P&L
- `pickNowOnly` - Only active picks (boolean)

### GET /api/strategies/[strategy]
Returns detailed time-series data for a specific strategy.

Query parameters:
- `date` - Date string
- `product` - Product filter

## License

Private - Internal use only

