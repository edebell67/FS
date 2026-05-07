import { Top20Data, DashboardMetrics, TopStrategy } from '@/types'

export function calculateDashboardMetrics(top20: Top20Data): DashboardMetrics {
  const strategies = top20.top20

  const totalNet = strategies.reduce((sum, s) => sum + s.total_net, 0)
  const avgWinRate = strategies.length > 0
    ? strategies.reduce((sum, s) => sum + (s.buyPercent + s.sellPercent) / 2, 0) / strategies.length
    : 0
  const activePicks = strategies.filter(s => s.pick_now).length

  const productBreakdown: { [key: string]: number } = {}
  strategies.forEach(s => {
    const baseProduct = s.product.replace(/_[CS]$/, '')
    productBreakdown[baseProduct] = (productBreakdown[baseProduct] || 0) + s.total_net
  })

  const topPerformer = strategies.length > 0
    ? strategies.reduce((max, s) => s.total_net > max.total_net ? s : max, strategies[0])
    : null

  return {
    totalStrategies: strategies.length,
    topPerformer,
    totalNet,
    avgWinRate,
    activePicks,
    productBreakdown,
  }
}

export function filterStrategies(
  strategies: TopStrategy[],
  filters: {
    strategy?: string
    product?: string
    minNet?: number | null
    maxNet?: number | null
    pickNowOnly?: boolean
  }
): TopStrategy[] {
  return strategies.filter(s => {
    if (filters.strategy && !s.strategy.toLowerCase().includes(filters.strategy.toLowerCase())) {
      return false
    }
    if (filters.product && !s.product.toLowerCase().includes(filters.product.toLowerCase())) {
      return false
    }
    if (filters.minNet !== null && filters.minNet !== undefined && s.total_net < filters.minNet) {
      return false
    }
    if (filters.maxNet !== null && filters.maxNet !== undefined && s.total_net > filters.maxNet) {
      return false
    }
    if (filters.pickNowOnly && !s.pick_now) {
      return false
    }
    return true
  })
}

export function getSignificantMovers(strategies: TopStrategy[], threshold: number = 100): TopStrategy[] {
  return strategies.filter(s => Math.abs(s.total_net) >= threshold)
    .sort((a, b) => Math.abs(b.total_net) - Math.abs(a.total_net))
}
