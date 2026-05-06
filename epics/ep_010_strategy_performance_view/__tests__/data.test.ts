import {
  filterStrategies,
  calculateDashboardMetrics,
  extractProductType,
  getSignificantMovers,
} from '@/lib/data'
import { TopStrategy, Top20Data } from '@/types'

const mockStrategies: TopStrategy[] = [
  {
    strategy: 'breakout_2_tp30.0_sl10.0',
    product: 'GBPEUR_S',
    total_net: 570,
    buy_net: 285,
    sell_net: 285,
    buy_count: 1,
    sell_count: 1,
    buyPercent: 100,
    sellPercent: 100,
    trade_count: 2,
    pick_now: true,
  },
  {
    strategy: 'breakout_3_tp20.0_sl5.0',
    product: 'EURUSD_C',
    total_net: -150,
    buy_net: -100,
    sell_net: -50,
    buy_count: 2,
    sell_count: 1,
    buyPercent: 50,
    sellPercent: 0,
    trade_count: 3,
    pick_now: false,
  },
  {
    strategy: 'breakout_2_tp15.0_sl10.0',
    product: 'GBPUSD_S',
    total_net: 200,
    buy_net: 100,
    sell_net: 100,
    buy_count: 2,
    sell_count: 2,
    buyPercent: 75,
    sellPercent: 75,
    trade_count: 4,
    pick_now: true,
  },
]

describe('Data Functions', () => {
  describe('filterStrategies', () => {
    it('filters by strategy name', () => {
      const result = filterStrategies(mockStrategies, { strategy: 'breakout_2' })
      expect(result).toHaveLength(2)
      expect(result.every(s => s.strategy.includes('breakout_2'))).toBe(true)
    })

    it('filters by product', () => {
      const result = filterStrategies(mockStrategies, { product: 'GBPEUR' })
      expect(result).toHaveLength(1)
      expect(result[0].product).toBe('GBPEUR_S')
    })

    it('filters by minimum net', () => {
      const result = filterStrategies(mockStrategies, { minNet: 100 })
      expect(result).toHaveLength(2)
      expect(result.every(s => s.total_net >= 100)).toBe(true)
    })

    it('filters by maximum net', () => {
      const result = filterStrategies(mockStrategies, { maxNet: 300 })
      expect(result).toHaveLength(2)
      expect(result.every(s => s.total_net <= 300)).toBe(true)
    })

    it('filters by pick_now only', () => {
      const result = filterStrategies(mockStrategies, { pickNowOnly: true })
      expect(result).toHaveLength(2)
      expect(result.every(s => s.pick_now)).toBe(true)
    })

    it('combines multiple filters', () => {
      const result = filterStrategies(mockStrategies, {
        strategy: 'breakout_2',
        minNet: 0,
        pickNowOnly: true,
      })
      expect(result).toHaveLength(2)
    })
  })

  describe('calculateDashboardMetrics', () => {
    const mockData: Top20Data = {
      last_update: '2026-04-03T23:59:51.801505',
      top20: mockStrategies,
    }

    it('calculates total strategies correctly', () => {
      const result = calculateDashboardMetrics(mockData)
      expect(result.totalStrategies).toBe(3)
    })

    it('calculates total net correctly', () => {
      const result = calculateDashboardMetrics(mockData)
      expect(result.totalNet).toBe(620)
    })

    it('identifies top performer correctly', () => {
      const result = calculateDashboardMetrics(mockData)
      expect(result.topPerformer?.strategy).toBe('breakout_2_tp30.0_sl10.0')
      expect(result.topPerformer?.total_net).toBe(570)
    })

    it('counts active picks correctly', () => {
      const result = calculateDashboardMetrics(mockData)
      expect(result.activePicks).toBe(2)
    })

    it('calculates product breakdown', () => {
      const result = calculateDashboardMetrics(mockData)
      expect(result.productBreakdown['GBPEUR']).toBe(570)
      expect(result.productBreakdown['EURUSD']).toBe(-150)
      expect(result.productBreakdown['GBPUSD']).toBe(200)
    })
  })

  describe('extractProductType', () => {
    it('removes suffix from product names', () => {
      expect(extractProductType('GBPEUR_S')).toBe('GBPEUR')
      expect(extractProductType('EURUSD_C')).toBe('EURUSD')
    })

    it('handles products without suffix', () => {
      expect(extractProductType('GBPEUR')).toBe('GBPEUR')
    })
  })

  describe('getSignificantMovers', () => {
    it('filters strategies above threshold', () => {
      const result = getSignificantMovers(mockStrategies, 100)
      expect(result).toHaveLength(3)
    })

    it('sorts by absolute value descending', () => {
      const result = getSignificantMovers(mockStrategies, 100)
      expect(result[0].total_net).toBe(570)
    })

    it('respects custom threshold', () => {
      const result = getSignificantMovers(mockStrategies, 500)
      expect(result).toHaveLength(1)
    })
  })
})
