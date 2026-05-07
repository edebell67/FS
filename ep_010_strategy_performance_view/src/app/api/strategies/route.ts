import { NextRequest, NextResponse } from 'next/server'
import { getTop20Data, getSummaryNetData, getAvailableDates, calculateDashboardMetrics, filterStrategies } from '@/lib/data'

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams
  const date = searchParams.get('date') || '2026-04-03'
  const strategy = searchParams.get('strategy') || ''
  const product = searchParams.get('product') || ''
  const minNet = searchParams.get('minNet')
  const maxNet = searchParams.get('maxNet')
  const pickNowOnly = searchParams.get('pickNowOnly') === 'true'

  try {
    const [top20Data, availableDates] = await Promise.all([
      getTop20Data(date),
      getAvailableDates(),
    ])

    if (!top20Data) {
      return NextResponse.json(
        { error: 'Data not found for the specified date' },
        { status: 404 }
      )
    }

    const filteredStrategies = filterStrategies(top20Data.top20, {
      strategy,
      product,
      minNet: minNet ? Number(minNet) : null,
      maxNet: maxNet ? Number(maxNet) : null,
      pickNowOnly,
    })

    const metrics = calculateDashboardMetrics({
      ...top20Data,
      top20: filteredStrategies,
    })

    const allProducts = Array.from(new Set(top20Data.top20.map(s => s.product))).sort()

    return NextResponse.json({
      strategies: filteredStrategies,
      allStrategies: top20Data.top20,
      metrics,
      products: allProducts,
      lastUpdate: top20Data.last_update,
      availableDates,
      currentDate: date,
    })
  } catch (error) {
    console.error('API Error:', error)
    return NextResponse.json(
      { error: 'Failed to fetch strategy data' },
      { status: 500 }
    )
  }
}
