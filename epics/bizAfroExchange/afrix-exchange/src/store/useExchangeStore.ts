'use client';

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Market, Order, Position, OrderBook, Trade } from '@/types';

interface ExchangeState {
  // Market data
  selectedMarket: Market | null;
  markets: Market[];
  orderBook: OrderBook | null;
  recentTrades: Trade[];

  // User data
  orders: Order[];
  positions: Position[];
  favorites: string[];

  // Actions
  setSelectedMarket: (market: Market) => void;
  setMarkets: (markets: Market[]) => void;
  setOrderBook: (orderBook: OrderBook) => void;
  setRecentTrades: (trades: Trade[]) => void;
  addOrder: (order: Order) => void;
  cancelOrder: (orderId: string) => void;
  updateOrder: (orderId: string, updates: Partial<Order>) => void;
  toggleFavorite: (marketId: string) => void;
  setPositions: (positions: Position[]) => void;
}

export const useExchangeStore = create<ExchangeState>()(
  persist(
    (set) => ({
      // Initial state
      selectedMarket: null,
      markets: [],
      orderBook: null,
      recentTrades: [],
      orders: [],
      positions: [
        {
          market: 'sNGN/sKES',
          side: 'long',
          size: 10000,
          avgEntryPrice: 0.2834,
          currentPrice: 0.2856,
          unrealizedPnL: 22.0,
          unrealizedPnLPercent: 0.78,
        },
        {
          market: 'sZAR/sGHS',
          side: 'short',
          size: 500,
          avgEntryPrice: 0.8290,
          currentPrice: 0.8234,
          unrealizedPnL: 28.0,
          unrealizedPnLPercent: 0.68,
        },
      ],
      favorites: ['sNGN_sKES', 'sZAR_sGHS'],

      // Actions
      setSelectedMarket: (market) => set({ selectedMarket: market }),

      setMarkets: (markets) => set({ markets }),

      setOrderBook: (orderBook) => set({ orderBook }),

      setRecentTrades: (trades) => set({ recentTrades: trades }),

      addOrder: (order) =>
        set((state) => ({
          orders: [order, ...state.orders],
        })),

      cancelOrder: (orderId) =>
        set((state) => ({
          orders: state.orders.map((o) =>
            o.id === orderId ? { ...o, status: 'cancelled' as const } : o
          ),
        })),

      updateOrder: (orderId, updates) =>
        set((state) => ({
          orders: state.orders.map((o) =>
            o.id === orderId ? { ...o, ...updates } : o
          ),
        })),

      toggleFavorite: (marketId) =>
        set((state) => ({
          favorites: state.favorites.includes(marketId)
            ? state.favorites.filter((id) => id !== marketId)
            : [...state.favorites, marketId],
        })),

      setPositions: (positions) => set({ positions }),
    }),
    {
      name: 'afrix-exchange-storage',
      partialize: (state) => ({
        favorites: state.favorites,
        orders: state.orders.filter((o) => o.status === 'open'),
      }),
    }
  )
);
