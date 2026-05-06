'use client'

import { useState } from 'react'
import { ChevronDown, ChevronUp, ExternalLink, Zap } from 'lucide-react'
import { TopStrategy } from '@/types'
import { useStore } from '@/hooks/useStore'
import { cn, formatCurrency, formatPercent, getNetColorClass, parseStrategyName } from '@/lib/utils'

interface StrategiesTableProps {
  strategies: TopStrategy[]
  onSelectStrategy: (strategy: TopStrategy) => void
}

type SortField = 'strategy' | 'product' | 'total_net' | 'buyPercent' | 'sellPercent' | 'trade_count'
type SortDirection = 'asc' | 'desc'

export function StrategiesTable({ strategies, onSelectStrategy }: StrategiesTableProps) {
  const { user, setShowAuthModal, isGated } = useStore()
  const [sortField, setSortField] = useState<SortField>('total_net')
  const [sortDirection, setSortDirection] = useState<SortDirection>('desc')

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('desc')
    }
  }

  const sortedStrategies = [...strategies].sort((a, b) => {
    let aVal = a[sortField]
    let bVal = b[sortField]

    if (typeof aVal === 'string') {
      aVal = aVal.toLowerCase()
      bVal = (bVal as string).toLowerCase()
    }

    if (aVal < bVal) return sortDirection === 'asc' ? -1 : 1
    if (aVal > bVal) return sortDirection === 'asc' ? 1 : -1
    return 0
  })

  const displayStrategies = isGated && !user ? sortedStrategies.slice(0, 5) : sortedStrategies

  const SortHeader = ({ field, children }: { field: SortField; children: React.ReactNode }) => (
    <button
      onClick={() => handleSort(field)}
      className="flex items-center gap-1 table-header hover:text-ink transition-colors group"
    >
      {children}
      <span className={cn(
        'transition-opacity',
        sortField === field ? 'opacity-100' : 'opacity-0 group-hover:opacity-50'
      )}>
        {sortField === field && sortDirection === 'asc' ? (
          <ChevronUp className="w-3 h-3" />
        ) : (
          <ChevronDown className="w-3 h-3" />
        )}
      </span>
    </button>
  )

  return (
    <div className="card overflow-hidden p-0">
      <div className="overflow-x-auto scrollbar-hide">
        <table className="w-full min-w-[800px]">
          <thead>
            <tr className="border-b border-whisper bg-gray-50/50">
              <th className="table-cell">
                <SortHeader field="strategy">Strategy</SortHeader>
              </th>
              <th className="table-cell">
                <SortHeader field="product">Product</SortHeader>
              </th>
              <th className="table-cell text-right">
                <SortHeader field="total_net">Net P&L</SortHeader>
              </th>
              <th className="table-cell text-right hidden md:table-cell">
                <SortHeader field="buyPercent">Buy Win%</SortHeader>
              </th>
              <th className="table-cell text-right hidden md:table-cell">
                <SortHeader field="sellPercent">Sell Win%</SortHeader>
              </th>
              <th className="table-cell text-right">
                <SortHeader field="trade_count">Trades</SortHeader>
              </th>
              <th className="table-cell text-center w-20">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-whisper">
            {displayStrategies.map((strategy, index) => {
              const parsed = parseStrategyName(strategy.strategy)
              return (
                <tr
                  key={`${strategy.strategy}-${strategy.product}-${index}`}
                  className="hover:bg-gray-50/50 transition-colors cursor-pointer group"
                  onClick={() => onSelectStrategy(strategy)}
                >
                  <td className="table-cell">
                    <div className="flex items-center gap-3">
                      <div>
                        <p className="font-medium text-ink">{parsed.type}</p>
                        <p className="text-xs text-muted font-mono">
                          v{parsed.version} TP:{parsed.tp} SL:{parsed.sl}
                        </p>
                      </div>
                    </div>
                  </td>
                  <td className="table-cell">
                    <span className="inline-flex items-center px-2.5 py-1 rounded-lg bg-gray-100 text-xs font-medium text-ink">
                      {strategy.product}
                    </span>
                  </td>
                  <td className={cn('table-cell text-right font-mono font-medium', getNetColorClass(strategy.total_net))}>
                    {formatCurrency(strategy.total_net)}
                  </td>
                  <td className="table-cell text-right font-mono text-steel hidden md:table-cell">
                    {formatPercent(strategy.buyPercent)}
                  </td>
                  <td className="table-cell text-right font-mono text-steel hidden md:table-cell">
                    {formatPercent(strategy.sellPercent)}
                  </td>
                  <td className="table-cell text-right font-mono text-steel">
                    {strategy.trade_count}
                  </td>
                  <td className="table-cell text-center">
                    {strategy.pick_now ? (
                      <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full bg-emerald-light text-emerald-signal text-xs font-medium">
                        <Zap className="w-3 h-3" />
                        Live
                      </span>
                    ) : (
                      <span className="text-muted text-xs">Inactive</span>
                    )}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {isGated && !user && strategies.length > 5 && (
        <div className="relative">
          <div className="absolute inset-x-0 -top-20 h-20 bg-gradient-to-t from-surface to-transparent pointer-events-none" />
          <div className="p-8 text-center bg-gray-50/50 border-t border-whisper">
            <p className="text-steel mb-4">
              Sign in to view all {strategies.length} strategies and detailed analytics
            </p>
            <div className="flex items-center justify-center gap-3">
              <button
                onClick={() => setShowAuthModal('signin')}
                className="btn-secondary"
              >
                Sign In
              </button>
              <button
                onClick={() => setShowAuthModal('signup')}
                className="btn-primary"
              >
                Get Started Free
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
