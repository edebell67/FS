'use client'

import { ReactNode } from 'react'
import { cn } from '@/lib/utils'
import { TrendingUp, TrendingDown, Minus } from 'lucide-react'

interface MetricCardProps {
  title: string
  value: string | number
  subtitle?: string
  trend?: 'up' | 'down' | 'neutral'
  trendValue?: string
  icon?: ReactNode
  className?: string
}

export function MetricCard({
  title,
  value,
  subtitle,
  trend,
  trendValue,
  icon,
  className,
}: MetricCardProps) {
  return (
    <div className={cn('card-compact', className)}>
      <div className="flex items-start justify-between mb-4">
        <span className="text-xs font-medium text-steel uppercase tracking-wider">
          {title}
        </span>
        {icon && (
          <div className="w-8 h-8 rounded-lg bg-gray-100 flex items-center justify-center text-steel">
            {icon}
          </div>
        )}
      </div>

      <div className="space-y-2">
        <p className="text-3xl md:text-4xl font-semibold text-ink tracking-tight font-mono">
          {value}
        </p>

        {(subtitle || trendValue) && (
          <div className="flex items-center gap-2">
            {trend && (
              <span
                className={cn(
                  'flex items-center gap-1 text-xs font-medium',
                  trend === 'up' && 'text-emerald-signal',
                  trend === 'down' && 'text-rose-deep',
                  trend === 'neutral' && 'text-steel'
                )}
              >
                {trend === 'up' && <TrendingUp className="w-3 h-3" />}
                {trend === 'down' && <TrendingDown className="w-3 h-3" />}
                {trend === 'neutral' && <Minus className="w-3 h-3" />}
                {trendValue}
              </span>
            )}
            {subtitle && (
              <span className="text-sm text-steel">{subtitle}</span>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

interface MetricBadgeProps {
  label: string
  value: string | number
  variant?: 'success' | 'danger' | 'neutral'
}

export function MetricBadge({ label, value, variant = 'neutral' }: MetricBadgeProps) {
  return (
    <div
      className={cn(
        'metric-badge',
        variant === 'success' && 'bg-emerald-light text-emerald-signal',
        variant === 'danger' && 'bg-rose-light text-rose-deep',
        variant === 'neutral' && 'bg-gray-100 text-steel'
      )}
    >
      <span className="mr-1">{label}:</span>
      <span className="font-semibold">{value}</span>
    </div>
  )
}
