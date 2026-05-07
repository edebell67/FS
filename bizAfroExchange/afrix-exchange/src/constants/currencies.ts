import { Currency, Market } from '@/types';

export const CURRENCIES: Currency[] = [
  { code: 'NGN', name: 'Nigerian Naira', syntheticSymbol: 'sNGN', region: 'West Africa', decimals: 2, flagEmoji: '🇳🇬' },
  { code: 'KES', name: 'Kenyan Shilling', syntheticSymbol: 'sKES', region: 'East Africa', decimals: 2, flagEmoji: '🇰🇪' },
  { code: 'ZAR', name: 'South African Rand', syntheticSymbol: 'sZAR', region: 'Southern Africa', decimals: 2, flagEmoji: '🇿🇦' },
  { code: 'GHS', name: 'Ghanaian Cedi', syntheticSymbol: 'sGHS', region: 'West Africa', decimals: 2, flagEmoji: '🇬🇭' },
  { code: 'EGP', name: 'Egyptian Pound', syntheticSymbol: 'sEGP', region: 'North Africa', decimals: 2, flagEmoji: '🇪🇬' },
  { code: 'MAD', name: 'Moroccan Dirham', syntheticSymbol: 'sMAD', region: 'North Africa', decimals: 2, flagEmoji: '🇲🇦' },
  { code: 'TZS', name: 'Tanzanian Shilling', syntheticSymbol: 'sTZS', region: 'East Africa', decimals: 2, flagEmoji: '🇹🇿' },
  { code: 'UGX', name: 'Ugandan Shilling', syntheticSymbol: 'sUGX', region: 'East Africa', decimals: 0, flagEmoji: '🇺🇬' },
  { code: 'XOF', name: 'West African CFA Franc', syntheticSymbol: 'sXOF', region: 'West Africa', decimals: 0, flagEmoji: '🌍' },
  { code: 'XAF', name: 'Central African CFA Franc', syntheticSymbol: 'sXAF', region: 'Central Africa', decimals: 0, flagEmoji: '🌍' },
  { code: 'ETB', name: 'Ethiopian Birr', syntheticSymbol: 'sETB', region: 'East Africa', decimals: 2, flagEmoji: '🇪🇹' },
  { code: 'RWF', name: 'Rwandan Franc', syntheticSymbol: 'sRWF', region: 'East Africa', decimals: 0, flagEmoji: '🇷🇼' },
];

export const getCurrency = (code: string): Currency | undefined => {
  return CURRENCIES.find(c => c.code === code || c.syntheticSymbol === code);
};

export const MARKETS: Market[] = [
  {
    id: 'sNGN_sKES',
    symbol: 'sNGN/sKES',
    base: CURRENCIES[0],  // NGN
    quote: CURRENCIES[1], // KES
    tickSize: 0.0001,
    minOrderSize: 100,
    makerFee: 0.001,
    takerFee: 0.002,
    lastPrice: 0.2856,
    change24h: 2.34,
    volume24h: 1250000,
  },
  {
    id: 'sZAR_sGHS',
    symbol: 'sZAR/sGHS',
    base: CURRENCIES[2],  // ZAR
    quote: CURRENCIES[3], // GHS
    tickSize: 0.0001,
    minOrderSize: 10,
    makerFee: 0.001,
    takerFee: 0.002,
    lastPrice: 0.8234,
    change24h: -1.12,
    volume24h: 890000,
  },
  {
    id: 'sEGP_sMAD',
    symbol: 'sEGP/sMAD',
    base: CURRENCIES[4],  // EGP
    quote: CURRENCIES[5], // MAD
    tickSize: 0.0001,
    minOrderSize: 50,
    makerFee: 0.001,
    takerFee: 0.002,
    lastPrice: 0.2045,
    change24h: 0.56,
    volume24h: 650000,
  },
  {
    id: 'sNGN_sZAR',
    symbol: 'sNGN/sZAR',
    base: CURRENCIES[0],  // NGN
    quote: CURRENCIES[2], // ZAR
    tickSize: 0.00001,
    minOrderSize: 100,
    makerFee: 0.001,
    takerFee: 0.002,
    lastPrice: 0.0112,
    change24h: 1.89,
    volume24h: 780000,
  },
  {
    id: 'sKES_sTZS',
    symbol: 'sKES/sTZS',
    base: CURRENCIES[1],  // KES
    quote: CURRENCIES[6], // TZS
    tickSize: 0.01,
    minOrderSize: 100,
    makerFee: 0.001,
    takerFee: 0.002,
    lastPrice: 19.85,
    change24h: -0.45,
    volume24h: 320000,
  },
  {
    id: 'sGHS_sNGN',
    symbol: 'sGHS/sNGN',
    base: CURRENCIES[3],  // GHS
    quote: CURRENCIES[0], // NGN
    tickSize: 0.01,
    minOrderSize: 10,
    makerFee: 0.001,
    takerFee: 0.002,
    lastPrice: 125.45,
    change24h: 3.21,
    volume24h: 456000,
  },
  {
    id: 'sZAR_sKES',
    symbol: 'sZAR/sKES',
    base: CURRENCIES[2],  // ZAR
    quote: CURRENCIES[1], // KES
    tickSize: 0.01,
    minOrderSize: 10,
    makerFee: 0.001,
    takerFee: 0.002,
    lastPrice: 7.23,
    change24h: 0.78,
    volume24h: 540000,
  },
  {
    id: 'sETB_sKES',
    symbol: 'sETB/sKES',
    base: CURRENCIES[10], // ETB
    quote: CURRENCIES[1], // KES
    tickSize: 0.0001,
    minOrderSize: 50,
    makerFee: 0.001,
    takerFee: 0.002,
    lastPrice: 2.15,
    change24h: -0.89,
    volume24h: 210000,
  },
  {
    id: 'sRWF_sUGX',
    symbol: 'sRWF/sUGX',
    base: CURRENCIES[11], // RWF
    quote: CURRENCIES[7], // UGX
    tickSize: 0.01,
    minOrderSize: 1000,
    makerFee: 0.001,
    takerFee: 0.002,
    lastPrice: 3.42,
    change24h: 1.45,
    volume24h: 180000,
  },
  {
    id: 'sXOF_sXAF',
    symbol: 'sXOF/sXAF',
    base: CURRENCIES[8],  // XOF
    quote: CURRENCIES[9], // XAF
    tickSize: 0.0001,
    minOrderSize: 1000,
    makerFee: 0.0005,
    takerFee: 0.001,
    lastPrice: 1.0000,
    change24h: 0.00,
    volume24h: 950000,
  },
];

export const FEATURED_MARKETS = ['sNGN_sKES', 'sZAR_sGHS', 'sEGP_sMAD'];

export const SETTLEMENT_TOKEN = 'SETTLE';
