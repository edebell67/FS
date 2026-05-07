'use client'

import { X, TrendingUp, TrendingDown, Activity, BarChart3, Calendar } from 'lucide-react'
import { TopStrategy, SummaryEntry } from '@/types'
import { useStore } from '@/hooks/useStore'
import { cn, formatCurrency, formatPercent, getNetColorClass, parseStrategyName, formatDate, formatTime } from '@/lib/utils'
import { PerformanceChart } from './PerformanceChart'

interface StrategyDetailProps {
  strategy: TopStrategy
  summaryData?: SummaryEntry[]
  onClose: () => void
}

export function StrategyDetail({ strategy, summaryData, onClose }: StrategyDetailProps) {
  const { user, setShowAuthModal, timeFrame, setTimeFrame } = useStore()
  const parsed = parseStrategyName(strategy.strategy)

  const chartData = summaryData?.map((entry, index) => ({
    name: formatTime(entry.t),
    value: entry.net,
  })) || []

  const isGated = !user

  return (
    <div className="card animate-slide-up">
      <div className="flex items-start justify-between mb-6">
        <div>
          <div className="flex items-center gap-3 mb-2">
            <h3 className="text-xl font-semibold text-ink tracking-tight">{parsed.type}</h3>
            {strategy.pick_now && (
              <span className="metric-badge bg-emerald-light text-emerald-signal">
                <Activity className="w-3 h-3 mr-1" />
                Live
              </span>
            )}
          </div>
          <p className="text-steel">
            <span className="font-mono text-sm">v{parsed.version}</span>
            <span className="mx-2 text-muted">|</span>
            <span className="font-mono text-sm">TP: {parsed.tp} SL: {parsed.sl}</span>
            <span className="mx-2 text-muted">|</span>
            <span className="font-medium">{strategy.product}</span>
          </p>
        </div>
        <button
          onClick={onClose}
          className="p-2 -mr-2 text-steel hover:text-ink hover:bg-gray-100 rounded-lg transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <StatBox
          label="Total Net"
          value={formatCurrency(strategy.total_net)}
          trend={strategy.total_net >= 0 ? 'up' : 'down'}
        />
        <StatBox
          label="Buy Net"
          value={formatCurrency(strategy.buy_net)}
          trend={strategy.buy_net >= 0 ? 'up' : 'down'}
        />
        <StatBox
          label="Sell Net"
          value={formatCurrency(strategy.sell_net)}
          trend={strategy.sell_net >= 0 ? 'up' : 'down'}
        />
        <StatBox
          label="Total Trades"
          value={strategy.trade_count.toString()}
        />
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        <StatBox
          label="Buy Win Rate"
          value={formatPercent(strategy.buyPercent)}
          subtitle={`${strategy.buy_count} trades`}
        />
        <StatBox
          label="Sell Win Rate"
          value={formatPercent(strategy.sellPercent)}
          subtitle={`${strategy.sell_count} trades`}
        />
        <StatBox
          label="Avg Per Trade"
          value={formatCurrency(strategy.trade_count > 0 ? strategy.total_net / strategy.trade_count : 0)}
        />
        <StatBox
          label="Win Rate"
          value={formatPercent((strategy.buyPercent + strategy.sellPercent) / 2)}
        />
      </div>

      <div className="border-t border-whisper pt-6">
        <div className="flex items-center justify-between mb-4">
          <h4 className="font-medium text-ink flex items-center gap-2">
            <BarChart3 className="w-4 h-4 text-steel" />
            Performance Over Time
          </h4>
          <div className="flex items-center gap-1 p-1 bg-gray-100 rounded-lg">
            <button
              onClick={() => setTimeFrame('daily')}
              className={cn(
                'px-3 py-1.5 text-xs font-medium rounded-md transition-colors',
                timeFrame === 'daily' ? 'bg-surface shadow-sm text-ink' : 'text-steel hover:text-ink'
              )}
            >
              Daily
            </button>
            <button
              onClick={() => setTimeFrame('weekly')}
              className={cn(
                'px-3 py-1.5 text-xs font-medium rounded-md transition-colors',
                timeFrame === 'weekly' ? 'bg-surface shadow-sm text-ink' : 'text-steel hover:text-ink'
              )}
            >
              Weekly
            </button>
          </div>
        </div>

        {isGated ? (
          <div className="relative">
            <div className="blur-sm pointer-events-none">
              <div className="h-64 bg-gradient-to-br from-gray-100 to-gray-50 rounded-xl flex items-center justify-center">
                <div className="w-full max-w-md mx-auto">
                  <div className="h-32 border-l-2 border-b-2 border-gray-200 relative">
                    <svg className="w-full h-full" viewBox="0 0 400 120">
                      <path
                        d="M0,100 Q50,80 100,60 T200,40 T300,50 T400,20"
                        fill="none"
                        stroke="#10B981"
                        strokeWidth="2"
                        strokeDasharray="5,5"
                      />
                    </svg>
                  </div>
                </div>
              </div>
            </div>
            <div className="absolute inset-0 flex items-center justify-center bg-surface/80 backdrop-blur-sm rounded-xl">
              <div className="text-center p-6">
                <Calendar className="w-10 h-10 text-steel mx-auto mb-3" />
                <h4 className="font-semibold text-ink mb-2">Detailed Analytics Locked</h4>
                <p className="text-sm text-steel mb-4 max-w-xs">
                  Sign in to access {timeFrame} performance charts and historical data
                </p>
                <div className="flex items-center justify-center gap-3">
                  <button
                    onClick={() => setShowAuthModal('signin')}
                    className="btn-secondary text-sm px-4 py-2"
                  >
                    Sign In
                  </button>
                  <button
                    onClick={() => setShowAuthModal('signup')}
                    className="btn-primary text-sm px-4 py-2"
                  >
                    Get Started
                  </button>
                </div>
              </div>
            </div>
          </div>
        ) : chartData.length > 0 ? (
          <PerformanceChart data={chartData} height={280} />
        ) : (
          <div className="h-64 bg-gray-50 rounded-xl flex items-center justify-center">
            <p className="text-steel">No historical data available</p>
          </div>
        )}
      </div>
    </div>
  )
}

function StatBox({
  label,
  value,
  trend,
  subtitle,
}: {
  label: string
  value: string
  trend?: 'up' | 'down'
  subtitle?: string
}) {
  return (
    <div className="p-4 bg-gray-50 rounded-xl">
      <p className="text-xs font-medium text-steel uppercase tracking-wider mb-2">{label}</p>
      <div className="flex items-center gap-2">
        {trend && (
          trend === 'up' ? (
            <TrendingUp className="w-4 h-4 text-emerald-signal" />
          ) : (
            <TrendingDown className="w-4 h-4 text-rose-deep" />
          )
        )}
        <p className={cn(
          'text-lg font-semibold font-mono',
          trend === 'up' && 'text-emerald-signal',
          trend === 'down' && 'text-rose-deep',
          !trend && 'text-ink'
        )}>
          {value}
        </p>
      </div>
      {subtitle && <p className="text-xs text-muted mt-1">{subtitle}</p>}
    </div>
  )
}
