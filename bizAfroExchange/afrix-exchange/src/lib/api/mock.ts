import type { Market, OrderBook, Trade, Pool, Wallet, CandlestickData, LiquidityPosition } from '@/types';
import { MARKETS, CURRENCIES } from '@/constants/currencies';

// Helper functions
function delay(ms: number) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function randomWalk(value: number, volatility: number = 0.001): number {
  const change = (Math.random() - 0.5) * 2 * volatility * value;
  return Math.max(0.00001, value + change);
}

// Generate mock order book
function generateMockOrderBook(marketId: string): OrderBook {
  const market = MARKETS.find(m => m.id === marketId);
  const midPrice = market?.lastPrice || 1.0;
  const spread = midPrice * 0.001;

  const bids: { price: number; size: number; total?: number }[] = [];
  const asks: { price: number; size: number; total?: number }[] = [];

  let bidTotal = 0;
  let askTotal = 0;

  for (let i = 0; i < 15; i++) {
    const bidSize = Math.floor(Math.random() * 5000 + 500);
    const askSize = Math.floor(Math.random() * 5000 + 500);
    bidTotal += bidSize;
    askTotal += askSize;

    bids.push({
      price: midPrice - spread - (i * midPrice * 0.0005),
      size: bidSize,
      total: bidTotal,
    });

    asks.push({
      price: midPrice + spread + (i * midPrice * 0.0005),
      size: askSize,
      total: askTotal,
    });
  }

  return {
    market: marketId,
    bids,
    asks,
    spread: asks[0].price - bids[0].price,
    timestamp: Date.now(),
  };
}

// Generate mock trades
function generateMockTrades(marketId: string, count: number = 20): Trade[] {
  const market = MARKETS.find(m => m.id === marketId);
  const basePrice = market?.lastPrice || 1.0;
  const trades: Trade[] = [];

  for (let i = 0; i < count; i++) {
    trades.push({
      id: `trade_${Date.now()}_${i}`,
      market: marketId,
      price: randomWalk(basePrice, 0.002),
      size: Math.floor(Math.random() * 1000 + 100),
      side: Math.random() > 0.5 ? 'buy' : 'sell',
      timestamp: Date.now() - i * 30000,
    });
  }

  return trades;
}

// Generate mock candlestick data
function generateMockCandles(marketId: string, interval: string, count: number = 100): CandlestickData[] {
  const market = MARKETS.find(m => m.id === marketId);
  let price = market?.lastPrice || 1.0;
  const candles: CandlestickData[] = [];

  const intervalMs = {
    '1m': 60000,
    '5m': 300000,
    '15m': 900000,
    '1h': 3600000,
    '4h': 14400000,
    '1d': 86400000,
  }[interval] || 3600000;

  const now = Date.now();

  for (let i = count - 1; i >= 0; i--) {
    const open = price;
    const volatility = 0.005;
    const high = open * (1 + Math.random() * volatility);
    const low = open * (1 - Math.random() * volatility);
    const close = low + Math.random() * (high - low);

    candles.push({
      time: Math.floor((now - i * intervalMs) / 1000),
      open: Number(open.toFixed(6)),
      high: Number(high.toFixed(6)),
      low: Number(low.toFixed(6)),
      close: Number(close.toFixed(6)),
      volume: Math.floor(Math.random() * 100000 + 10000),
    });

    price = close;
  }

  return candles;
}

// Generate mock pools
function generateMockPools(): Pool[] {
  return [
    {
      id: 'pool_sNGN_sKES',
      pair: 'sNGN/sKES',
      base: CURRENCIES[0],
      quote: CURRENCIES[1],
      tvl: 1234567,
      volume24h: 450000,
      apr: 0.125,
      feeTier: 0.003,
      reserve0: 5000000,
      reserve1: 1428000,
      lpTotalSupply: 2670000,
      price: 0.2856,
    },
    {
      id: 'pool_sZAR_sGHS',
      pair: 'sZAR/sGHS',
      base: CURRENCIES[2],
      quote: CURRENCIES[3],
      tvl: 890000,
      volume24h: 320000,
      apr: 0.083,
      feeTier: 0.003,
      reserve0: 500000,
      reserve1: 411700,
      lpTotalSupply: 453300,
      price: 0.8234,
    },
    {
      id: 'pool_sEGP_sMAD',
      pair: 'sEGP/sMAD',
      base: CURRENCIES[4],
      quote: CURRENCIES[5],
      tvl: 650000,
      volume24h: 180000,
      apr: 0.151,
      feeTier: 0.003,
      reserve0: 1500000,
      reserve1: 306750,
      lpTotalSupply: 678000,
      price: 0.2045,
    },
    {
      id: 'pool_sNGN_sZAR',
      pair: 'sNGN/sZAR',
      base: CURRENCIES[0],
      quote: CURRENCIES[2],
      tvl: 520000,
      volume24h: 145000,
      apr: 0.095,
      feeTier: 0.003,
      reserve0: 23000000,
      reserve1: 257600,
      lpTotalSupply: 2430000,
      price: 0.0112,
    },
    {
      id: 'pool_sKES_sTZS',
      pair: 'sKES/sTZS',
      base: CURRENCIES[1],
      quote: CURRENCIES[6],
      tvl: 380000,
      volume24h: 98000,
      apr: 0.068,
      feeTier: 0.003,
      reserve0: 10000,
      reserve1: 198500,
      lpTotalSupply: 44500,
      price: 19.85,
    },
  ];
}

// Generate mock liquidity positions
function generateMockLiquidityPositions(): LiquidityPosition[] {
  return [
    {
      poolId: 'pool_sNGN_sKES',
      lpTokens: 5340,
      share: 0.002,
      value: 2469.13,
      unclaimedFees: 12.34,
    },
    {
      poolId: 'pool_sZAR_sGHS',
      lpTokens: 2267,
      share: 0.005,
      value: 4450.00,
      unclaimedFees: 8.50,
    },
  ];
}

// Mock API object
export const mockAPI = {
  getMarkets: async (): Promise<Market[]> => {
    await delay(100);
    return MARKETS.map(m => ({
      ...m,
      lastPrice: randomWalk(m.lastPrice || 1, 0.001),
      change24h: m.change24h! + (Math.random() - 0.5) * 0.1,
    }));
  },

  getMarket: async (marketId: string): Promise<Market | undefined> => {
    await delay(50);
    return MARKETS.find(m => m.id === marketId);
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

  getPool: async (poolId: string): Promise<Pool | undefined> => {
    await delay(50);
    const pools = generateMockPools();
    return pools.find(p => p.id === poolId);
  },

  getLiquidityPositions: async (): Promise<LiquidityPosition[]> => {
    await delay(50);
    return generateMockLiquidityPositions();
  },

  getWallet: async (): Promise<Wallet> => {
    await delay(50);
    return {
      balances: {
        'SETTLE': 100000,
        'sNGN': 1245000,
        'sKES': 832000,
        'sZAR': 46800,
        'sGHS': 12500,
        'sEGP': 85000,
      },
      totalValue: 125450,
    };
  },

  getCandlestickData: async (marketId: string, interval: string): Promise<CandlestickData[]> => {
    await delay(100);
    return generateMockCandles(marketId, interval);
  },
};

export default mockAPI;
