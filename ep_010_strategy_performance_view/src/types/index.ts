export interface TopStrategy {
  strategy: string
  product: string
  total_net: number
  buy_net: number
  sell_net: number
  buy_count: number
  sell_count: number
  buyPercent: number
  sellPercent: number
  trade_count: number
  pick_now: boolean
}

export interface Top20Data {
  last_update: string
  top20: TopStrategy[]
}

export interface SummaryEntry {
  t: string
  net: number
  buy_net: number
  sell_net: number
  buy_alt: number
  sell_alt: number
  live_buy: number
  live_sell: number
  b_c: number
  s_c: number
  buyPercent: number
  sellPercent: number
}

export interface SummaryNetData {
  last_update: string
  session_max_net: number
  strategies: {
    [strategyKey: string]: {
      [productKey: string]: SummaryEntry[]
    }
  }
}

export interface FilterState {
  strategy: string
  product: string
  minNet: number | null
  maxNet: number | null
  pickNowOnly: boolean
}

export interface DashboardMetrics {
  totalStrategies: number
  topPerformer: TopStrategy | null
  totalNet: number
  avgWinRate: number
  activePicks: number
  productBreakdown: { [key: string]: number }
}

export interface User {
  email: string
  name: string
  isAuthenticated: boolean
}

export type TimeFrame = 'daily' | 'weekly'
