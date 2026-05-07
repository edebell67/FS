import {
  formatCurrency,
  formatPercent,
  formatDate,
  getNetColorClass,
  parseStrategyName,
  cn,
} from '@/lib/utils'

describe('Utility Functions', () => {
  describe('formatCurrency', () => {
    it('formats positive numbers with plus sign', () => {
      expect(formatCurrency(100)).toBe('+$100.00')
      expect(formatCurrency(1234.56)).toBe('+$1,234.56')
    })

    it('formats negative numbers with minus sign', () => {
      expect(formatCurrency(-100)).toBe('-$100.00')
      expect(formatCurrency(-1234.56)).toBe('-$1,234.56')
    })

    it('formats zero as positive', () => {
      expect(formatCurrency(0)).toBe('+$0.00')
    })
  })

  describe('formatPercent', () => {
    it('formats percentages with one decimal place', () => {
      expect(formatPercent(50)).toBe('50.0%')
      expect(formatPercent(33.333)).toBe('33.3%')
      expect(formatPercent(100)).toBe('100.0%')
    })
  })

  describe('formatDate', () => {
    it('formats date strings correctly', () => {
      const result = formatDate('2026-04-03T12:00:00')
      expect(result).toContain('Apr')
      expect(result).toContain('3')
      expect(result).toContain('2026')
    })
  })

  describe('getNetColorClass', () => {
    it('returns green for positive values', () => {
      expect(getNetColorClass(100)).toBe('text-emerald-signal')
    })

    it('returns red for negative values', () => {
      expect(getNetColorClass(-100)).toBe('text-rose-deep')
    })

    it('returns neutral for zero', () => {
      expect(getNetColorClass(0)).toBe('text-steel')
    })
  })

  describe('parseStrategyName', () => {
    it('parses valid strategy names', () => {
      const result = parseStrategyName('breakout_2_tp30.0_sl10.0')
      expect(result).toEqual({
        type: 'breakout',
        version: '2',
        tp: '30.0',
        sl: '10.0',
      })
    })

    it('handles invalid strategy names', () => {
      const result = parseStrategyName('invalid')
      expect(result).toEqual({
        type: 'invalid',
        version: '',
        tp: '',
        sl: '',
      })
    })
  })

  describe('cn', () => {
    it('merges class names', () => {
      expect(cn('foo', 'bar')).toBe('foo bar')
    })

    it('handles conditional classes', () => {
      expect(cn('foo', false && 'bar', 'baz')).toBe('foo baz')
    })
  })
})
