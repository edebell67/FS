'use client';

import { create } from 'zustand';
import type { Pool, LiquidityPosition } from '@/types';

interface LiquidityState {
  pools: Pool[];
  userPositions: LiquidityPosition[];
  selectedPool: Pool | null;

  setPools: (pools: Pool[]) => void;
  setUserPositions: (positions: LiquidityPosition[]) => void;
  setSelectedPool: (pool: Pool | null) => void;
}

export const useLiquidityStore = create<LiquidityState>((set) => ({
  pools: [],
  userPositions: [],
  selectedPool: null,

  setPools: (pools) => set({ pools }),
  setUserPositions: (positions) => set({ userPositions: positions }),
  setSelectedPool: (pool) => set({ selectedPool: pool }),
}));
