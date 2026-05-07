'use client'

import { useState, useEffect, useMemo } from 'react'
import {
  Navigation,
  AuthModal,
  Dashboard,
  FilterPanel,
  StrategiesTable,
  StrategyDetail,
} from '@/components'
import { useStore } from '@/hooks/useStore'
import { filterStrategies, calculateDashboardMetrics } from '@/lib/data-client'
import { TopStrategy, DashboardMetrics, SummaryEntry } from '@/types'
import { formatDate, formatTime } from '@/lib/utils'
import { RefreshCw, Calendar } from 'lucide-react'

interface ClientPageProps {
  initialStrategies: TopStrategy[]
  initialMetrics: DashboardMetrics
  products: string[]
  lastUpdate: string
}

export function ClientPage({
  initialStrategies,
  initialMetrics,
  products,
  lastUpdate,
}: ClientPageProps) {
  const { filters, selectedStrategy, setSelectedStrategy } = useStore()
  const [summaryData, setSummaryData] = useState<SummaryEntry[] | undefined>()
  const [loading, setLoading] = useState(false)

  const filteredStrategies = useMemo(() => {
    return filterStrategies(initialStrategies, filters)
  }, [initialStrategies, filters])

  const metrics = useMemo(() => {
    return calculateDashboardMetrics({ last_update: lastUpdate, top20: filteredStrategies })
  }, [filteredStrategies, lastUpdate])

  useEffect(() => {
    if (selectedStrategy) {
      setLoading(true)
      fetch(`/api/strategies/${encodeURIComponent(selectedStrategy.strategy)}?product=${selectedStrategy.product}`)
        .then(res => res.json())
        .then(data => {
          setSummaryData(data.entries || [])
        })
        .catch(console.error)
        .finally(() => setLoading(false))
    } else {
      setSummaryData(undefined)
    }
  }, [selectedStrategy])

  return (
    <div className="min-h-[100dvh] bg-canvas">
      <Navigation />
      <AuthModal />

      <main className="max-w-7xl mx-auto px-4 md:px-6 lg:px-8 py-8 md:py-12">
        <header className="mb-8 md:mb-12">
          <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4">
            <div>
              <h1 className="text-3xl md:text-4xl lg:text-5xl font-semibold text-ink tracking-tight text-balance">
                Strategy Performance
              </h1>
              <p className="text-steel mt-2 md:mt-3 text-lg">
                Real-time analytics for top trading strategies
              </p>
            </div>
            <div className="flex items-center gap-4 text-sm text-steel">
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4" />
                <span>{formatDate(lastUpdate)}</span>
              </div>
              <div className="flex items-center gap-2">
                <RefreshCw className="w-4 h-4" />
                <span>Updated {formatTime(lastUpdate)}</span>
              </div>
            </div>
          </div>
        </header>

        <section id="dashboard" className="mb-12 md:mb-16 scroll-mt-24">
          <Dashboard
            metrics={metrics}
            strategies={filteredStrategies}
            onSelectStrategy={setSelectedStrategy}
          />
        </section>

        {selectedStrategy && (
          <section className="mb-12 md:mb-16 scroll-mt-24">
            <StrategyDetail
              strategy={selectedStrategy}
              summaryData={summaryData}
              onClose={() => setSelectedStrategy(null)}
            />
          </section>
        )}

        <section id="strategies" className="mb-12 md:mb-16 scroll-mt-24">
          <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4 mb-6">
            <div>
              <h2 className="text-2xl md:text-3xl font-semibold text-ink tracking-tight">
                Top 20 Strategies
              </h2>
              <p className="text-steel mt-1">
                {filteredStrategies.length} strategies matching your filters
              </p>
            </div>
          </div>

          <FilterPanel products={products} />

          <StrategiesTable
            strategies={filteredStrategies}
            onSelectStrategy={setSelectedStrategy}
          />
        </section>

        <section id="returns" className="mb-12 md:mb-16 scroll-mt-24">
          <div className="card text-center py-12 md:py-16">
            <h2 className="text-2xl md:text-3xl font-semibold text-ink tracking-tight mb-3">
              Weekly Returns Analysis
            </h2>
            <p className="text-steel max-w-xl mx-auto mb-6">
              Dive deep into weekly and daily performance trends with detailed
              breakdowns by strategy and product type.
            </p>
            <div className="flex items-center justify-center gap-3">
              <button
                onClick={() => {
                  const { user, setShowAuthModal } = useStore.getState()
                  if (!user) setShowAuthModal('signup')
                }}
                className="btn-primary"
              >
                Unlock Full Analytics
              </button>
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-whisper bg-surface mt-16">
        <div className="max-w-7xl mx-auto px-4 md:px-6 lg:px-8 py-8 md:py-12">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
            <div>
              <p className="font-semibold text-ink">StrategyView</p>
              <p className="text-sm text-steel mt-1">
                Professional trading strategy analytics
              </p>
            </div>
            <div className="flex items-center gap-6 text-sm text-steel">
              <a href="#" className="hover:text-ink transition-colors">Privacy</a>
              <a href="#" className="hover:text-ink transition-colors">Terms</a>
              <a href="#" className="hover:text-ink transition-colors">Contact</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
