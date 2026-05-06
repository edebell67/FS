import { clsx, type ClassValue } from 'clsx'

export function cn(...inputs: ClassValue[]) {
  return clsx(inputs)
}

export function formatCurrency(value: number): string {
  const absValue = Math.abs(value)
  const sign = value >= 0 ? '+' : '-'
  return `${sign}$${absValue.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`
}

export function formatPercent(value: number): string {
  return `${value.toFixed(1)}%`
}

export function formatDate(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

export function formatTime(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
  })
}

export function getNetColorClass(value: number): string {
  if (value > 0) return 'text-emerald-signal'
  if (value < 0) return 'text-rose-deep'
  return 'text-steel'
}

export function getNetBgClass(value: number): string {
  if (value > 0) return 'bg-emerald-light'
  if (value < 0) return 'bg-rose-light'
  return 'bg-gray-100'
}

export function debounce<T extends (...args: unknown[]) => unknown>(
  fn: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: NodeJS.Timeout
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => fn(...args), delay)
  }
}

export function parseStrategyName(strategy: string): {
  type: string
  version: string
  tp: string
  sl: string
} {
  const match = strategy.match(/^(\w+)_(\d+)_tp([\d.]+)_sl([\d.]+)$/)
  if (match) {
    return {
      type: match[1],
      version: match[2],
      tp: match[3],
      sl: match[4],
    }
  }
  return { type: strategy, version: '', tp: '', sl: '' }
}

export function extractProductType(product: string): string {
  return product.replace(/_[CS]$/, '')
}
