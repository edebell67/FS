'use client'

import { TrendingUp, TrendingDown, ArrowRight } from 'lucide-react'
import { TopStrategy } from '@/types'
import { cn, formatCurrency, extractProductType } from '@/lib/utils'

interface SignificantMoversProps {
  strategies: TopStrategy[]
  onSelectStrategy: (strategy: TopStrategy) => void
}

export function SignificantMovers({ strategies, onSelectStrategy }: SignificantMoversProps) {
  const movers = strategies
    .filter(s => Math.abs(s.total_net) >= 100)
    .sort((a, b) => Math.abs(b.total_net) - Math.abs(a.total_net))
    .slice(0, 6)

  const gainers = movers.filter(s => s.total_net > 0)
  const losers = movers.filter(s => s.total_net < 0)

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div className="card-compact">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-8 h-8 rounded-lg bg-emerald-light flex items-center justify-center">
            <TrendingUp className="w-4 h-4 text-emerald-signal" />
          </div>
          <div>
            <h3 className="font-semibold text-ink">Top Gainers</h3>
            <p className="text-xs text-steel">Significant positive returns</p>
          </div>
        </div>

        <div className="space-y-2">
          {gainers.length > 0 ? (
            gainers.map((strategy, index) => (
              <MoverRow
                key={`${strategy.strategy}-${strategy.product}-${index}`}
                strategy={strategy}
                onClick={() => onSelectStrategy(strategy)}
              />
            ))
          ) : (
            <p className="text-sm text-muted py-4 text-center">No significant gainers today</p>
          )}
        </div>
      </div>

      <div className="card-compact">
        <div className="flex items-center gap-2 mb-4">
          <div className="w-8 h-8 rounded-lg bg-rose-light flex items-center justify-center">
            <TrendingDown className="w-4 h-4 text-rose-deep" />
          </div>
          <div>
            <h3 className="font-semibold text-ink">Top Losers</h3>
            <p className="text-xs text-steel">Strategies to watch</p>
          </div>
        </div>

        <div className="space-y-2">
          {losers.length > 0 ? (
            losers.map((strategy, index) => (
              <MoverRow
                key={`${strategy.strategy}-${strategy.product}-${index}`}
                strategy={strategy}
                onClick={() => onSelectStrategy(strategy)}
              />
            ))
          ) : (
            <p className="text-sm text-muted py-4 text-center">No significant losers today</p>
          )}
        </div>
      </div>
    </div>
  )
}

function MoverRow({ strategy, onClick }: { strategy: TopStrategy; onClick: () => void }) {
  const isPositive = strategy.total_net >= 0
  const productType = extractProductType(strategy.product)

  return (
    <button
      onClick={onClick}
      className="w-full flex items-center justify-between p-3 rounded-xl hover:bg-gray-50 transition-colors group"
    >
      <div className="flex items-center gap-3">
        <div
          className={cn(
            'w-10 h-10 rounded-xl flex items-center justify-center text-xs font-bold',
            isPositive ? 'bg-emerald-light text-emerald-signal' : 'bg-rose-light text-rose-deep'
          )}
        >
          {productType.slice(0, 3)}
        </div>
        <div className="text-left">
          <p className="font-medium text-ink text-sm">{productType}</p>
          <p className="text-xs text-muted">{strategy.trade_count} trades</p>
        </div>
      </div>

      <div className="flex items-center gap-3">
        <span
          className={cn(
            'font-mono font-semibold',
            isPositive ? 'text-emerald-signal' : 'text-rose-deep'
          )}
        >
          {formatCurrency(strategy.total_net)}
        </span>
        <ArrowRight className="w-4 h-4 text-muted group-hover:text-ink transition-colors" />
      </div>
    </button>
  )
}
