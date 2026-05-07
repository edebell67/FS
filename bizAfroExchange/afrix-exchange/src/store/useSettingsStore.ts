'use client';

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { UserSettings } from '@/types';

interface SettingsState extends UserSettings {
  updateSettings: (settings: Partial<UserSettings>) => void;
  resetSettings: () => void;
}

const defaultSettings: UserSettings = {
  network: 'testnet',
  displayCurrency: 'SETTLE',
  confirmLargeOrders: true,
  warnHighSlippage: true,
  slippageThreshold: 2,
  largeOrderThreshold: 1000,
};

export const useSettingsStore = create<SettingsState>()(
  persist(
    (set) => ({
      ...defaultSettings,

      updateSettings: (settings) =>
        set((state) => ({
          ...state,
          ...settings,
        })),

      resetSettings: () => set(defaultSettings),
    }),
    {
      name: 'afrix-settings-storage',
    }
  )
);
