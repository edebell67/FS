import { Top20Data, SummaryNetData, DashboardMetrics, TopStrategy } from '@/types'
import { promises as fs } from 'fs'
import path from 'path'

const DATA_BASE_PATH = 'C:/Users/edebe/eds/TradeApps/breakout/fs/json/live/forex'

export async function getAvailableDates(): Promise<string[]> {
  try {
    const dirs = await fs.readdir(DATA_BASE_PATH)
    return dirs.filter(d => /^\d{4}-\d{2}-\d{2}$/.test(d)).sort().reverse()
  } catch {
    return ['2026-04-03']
  }
}

export async function getTop20Data(date: string): Promise<Top20Data | null> {
  try {
    const filePath = path.join(DATA_BASE_PATH, date, '_top20.json')
    const data = await fs.readFile(filePath, 'utf-8')
    return JSON.parse(data) as Top20Data
  } catch (error) {
    console.error('Error reading top20 data:', error)
    return null
  }
}

export async function getSummaryNetData(date: string): Promise<SummaryNetData | null> {
  try {
    const filePath = path.join(DATA_BASE_PATH, date, '_summary_net.json')
    const data = await fs.readFile(filePath, 'utf-8')
    return JSON.parse(data) as SummaryNetData
  } catch (error) {
    console.error('Error reading summary net data:', error)
    return null
  }
}

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

export function extractProductType(product: string): string {
  return product.replace(/_[CS]$/, '')
}

export function getSignificantMovers(strategies: TopStrategy[], threshold: number = 100): TopStrategy[] {
  return strategies.filter(s => Math.abs(s.total_net) >= threshold)
    .sort((a, b) => Math.abs(b.total_net) - Math.abs(a.total_net))
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

export function aggregateWeeklyReturns(
  summaryData: SummaryNetData,
  strategyFilter?: string
): { date: string; net: number }[] {
  const dailyTotals: { [date: string]: number } = {}

  Object.entries(summaryData.strategies).forEach(([strategy, products]) => {
    if (strategyFilter && !strategy.includes(strategyFilter)) return

    Object.values(products).forEach(entries => {
      if (Array.isArray(entries) && entries.length > 0) {
        const lastEntry = entries[entries.length - 1]
        const date = lastEntry.t.split('T')[0]
        dailyTotals[date] = (dailyTotals[date] || 0) + lastEntry.net
      }
    })
  })

  return Object.entries(dailyTotals)
    .map(([date, net]) => ({ date, net }))
    .sort((a, b) => a.date.localeCompare(b.date))
}
