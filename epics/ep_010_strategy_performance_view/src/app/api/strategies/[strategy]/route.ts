import { NextRequest, NextResponse } from 'next/server'
import { getSummaryNetData } from '@/lib/data'

export async function GET(
  request: NextRequest,
  { params }: { params: { strategy: string } }
) {
  const searchParams = request.nextUrl.searchParams
  const date = searchParams.get('date') || '2026-04-03'
  const product = searchParams.get('product') || ''
  const strategyName = decodeURIComponent(params.strategy)

  try {
    const summaryData = await getSummaryNetData(date)

    if (!summaryData) {
      return NextResponse.json(
        { error: 'Summary data not found' },
        { status: 404 }
      )
    }

    const strategyData = summaryData.strategies[strategyName]

    if (!strategyData) {
      return NextResponse.json({
        strategy: strategyName,
        product,
        entries: [],
        message: 'No detailed data available for this strategy',
      })
    }

    const productData = product ? strategyData[product] : null
    const allEntries = productData || Object.values(strategyData).flat()

    return NextResponse.json({
      strategy: strategyName,
      product,
      entries: allEntries,
      lastUpdate: summaryData.last_update,
      sessionMaxNet: summaryData.session_max_net,
    })
  } catch (error) {
    console.error('API Error:', error)
    return NextResponse.json(
      { error: 'Failed to fetch strategy details' },
      { status: 500 }
    )
  }
}
