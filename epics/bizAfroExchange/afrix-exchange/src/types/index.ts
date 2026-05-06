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
  lastPrice?: number;
  change24h?: number;
  volume24h?: number;
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

export interface LiquidityPosition {
  poolId: string;
  lpTokens: number;
  share: number;           // percentage of pool
  value: number;           // in SETTLE
  unclaimedFees: number;
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

export interface UserSettings {
  network: 'mainnet' | 'testnet';
  displayCurrency: string;
  confirmLargeOrders: boolean;
  warnHighSlippage: boolean;
  slippageThreshold: number;
  largeOrderThreshold: number;
}
