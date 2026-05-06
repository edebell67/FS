import { getTop20Data, calculateDashboardMetrics } from '@/lib/data'
import { ClientPage } from './ClientPage'

export const dynamic = 'force-dynamic'
export const revalidate = 60

export default async function HomePage() {
  const date = '2026-04-03'
  const top20Data = await getTop20Data(date)

  if (!top20Data) {
    return (
      <div className="min-h-[100dvh] flex items-center justify-center bg-canvas">
        <div className="text-center">
          <h1 className="text-2xl font-semibold text-ink mb-2">Data Unavailable</h1>
          <p className="text-steel">Unable to load strategy data. Please try again later.</p>
        </div>
      </div>
    )
  }

  const metrics = calculateDashboardMetrics(top20Data)
  const allProducts = Array.from(new Set(top20Data.top20.map(s => s.product))).sort()

  return (
    <ClientPage
      initialStrategies={top20Data.top20}
      initialMetrics={metrics}
      products={allProducts}
      lastUpdate={top20Data.last_update}
    />
  )
}
