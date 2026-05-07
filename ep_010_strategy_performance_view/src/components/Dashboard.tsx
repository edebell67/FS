'use client'

import { DollarSign, Activity, TrendingUp, BarChart3, Users, Zap } from 'lucide-react'
import { DashboardMetrics, TopStrategy } from '@/types'
import { formatCurrency, formatPercent } from '@/lib/utils'
import { MetricCard } from './MetricCard'
import { ProductBreakdownChart } from './PerformanceChart'
import { SignificantMovers } from './SignificantMovers'

interface DashboardProps {
  metrics: DashboardMetrics
  strategies: TopStrategy[]
  onSelectStrategy: (strategy: TopStrategy) => void
}

export function Dashboard({ metrics, strategies, onSelectStrategy }: DashboardProps) {
  const topPerformerNet = metrics.topPerformer?.total_net || 0

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-2xl md:text-3xl font-semibold text-ink tracking-tight mb-2">
          Performance Overview
        </h2>
        <p className="text-steel">
          Top 20 strategy performance metrics for today
        </p>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 animate-stagger">
        <MetricCard
          title="Total Net P&L"
          value={formatCurrency(metrics.totalNet)}
          trend={metrics.totalNet >= 0 ? 'up' : 'down'}
          trendValue={metrics.totalNet >= 0 ? 'Profitable' : 'Loss'}
          icon={<DollarSign className="w-4 h-4" />}
        />
        <MetricCard
          title="Strategies"
          value={metrics.totalStrategies}
          subtitle="In top 20"
          icon={<BarChart3 className="w-4 h-4" />}
        />
        <MetricCard
          title="Avg Win Rate"
          value={formatPercent(metrics.avgWinRate)}
          trend={metrics.avgWinRate >= 50 ? 'up' : 'down'}
          icon={<TrendingUp className="w-4 h-4" />}
        />
        <MetricCard
          title="Active Picks"
          value={metrics.activePicks}
          subtitle="Live now"
          icon={<Zap className="w-4 h-4" />}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="card-compact">
            <div className="flex items-center gap-2 mb-4">
              <Activity className="w-5 h-5 text-steel" />
              <h3 className="font-semibold text-ink">Significant Movers</h3>
            </div>
            <SignificantMovers
              strategies={strategies}
              onSelectStrategy={onSelectStrategy}
            />
          </div>
        </div>

        <div className="card-compact">
          <div className="flex items-center gap-2 mb-4">
            <BarChart3 className="w-5 h-5 text-steel" />
            <h3 className="font-semibold text-ink">Product Breakdown</h3>
          </div>
          {Object.keys(metrics.productBreakdown).length > 0 ? (
            <ProductBreakdownChart
              data={metrics.productBreakdown}
              height={280}
            />
          ) : (
            <div className="h-64 flex items-center justify-center text-muted">
              No product data available
            </div>
          )}
        </div>
      </div>

      {metrics.topPerformer && (
        <div className="card bg-gradient-to-br from-ink to-zinc-800 text-white">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
            <div>
              <p className="text-xs font-medium text-gray-400 uppercase tracking-wider mb-2">
                Top Performer Today
              </p>
              <h3 className="text-2xl font-semibold tracking-tight mb-1">
                {metrics.topPerformer.strategy}
              </h3>
              <p className="text-gray-400">
                {metrics.topPerformer.product}
                <span className="mx-2">|</span>
                {metrics.topPerformer.trade_count} trades
              </p>
            </div>
            <div className="flex items-center gap-6">
              <div>
                <p className="text-xs text-gray-400 uppercase tracking-wider mb-1">Net P&L</p>
                <p className="text-3xl font-bold font-mono text-emerald-400">
                  {formatCurrency(topPerformerNet)}
                </p>
              </div>
              <button
                onClick={() => onSelectStrategy(metrics.topPerformer!)}
                className="px-6 py-3 bg-white text-ink rounded-xl font-medium hover:bg-gray-100 transition-colors"
              >
                View Details
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
