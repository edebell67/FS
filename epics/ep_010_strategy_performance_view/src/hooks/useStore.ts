import { create } from 'zustand'
import { FilterState, User, TimeFrame, TopStrategy } from '@/types'

interface AppState {
  filters: FilterState
  setFilter: <K extends keyof FilterState>(key: K, value: FilterState[K]) => void
  resetFilters: () => void

  selectedStrategy: TopStrategy | null
  setSelectedStrategy: (strategy: TopStrategy | null) => void

  timeFrame: TimeFrame
  setTimeFrame: (timeFrame: TimeFrame) => void

  user: User | null
  setUser: (user: User | null) => void

  showAuthModal: 'signin' | 'signup' | null
  setShowAuthModal: (modal: 'signin' | 'signup' | null) => void

  isGated: boolean
  setIsGated: (gated: boolean) => void
}

const defaultFilters: FilterState = {
  strategy: '',
  product: '',
  minNet: null,
  maxNet: null,
  pickNowOnly: false,
}

export const useStore = create<AppState>((set) => ({
  filters: defaultFilters,
  setFilter: (key, value) =>
    set((state) => ({
      filters: { ...state.filters, [key]: value },
    })),
  resetFilters: () => set({ filters: defaultFilters }),

  selectedStrategy: null,
  setSelectedStrategy: (strategy) => set({ selectedStrategy: strategy }),

  timeFrame: 'daily',
  setTimeFrame: (timeFrame) => set({ timeFrame }),

  user: null,
  setUser: (user) => set({ user, isGated: !user }),

  showAuthModal: null,
  setShowAuthModal: (modal) => set({ showAuthModal: modal }),

  isGated: true,
  setIsGated: (gated) => set({ isGated: gated }),
}))
