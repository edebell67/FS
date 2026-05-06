'use client'

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
} from 'recharts'
import { formatCurrency } from '@/lib/utils'

interface ChartDataPoint {
  name: string
  value: number
  positive?: number
  negative?: number
}

interface PerformanceChartProps {
  data: ChartDataPoint[]
  type?: 'area' | 'bar'
  height?: number
}

export function PerformanceChart({ data, type = 'area', height = 300 }: PerformanceChartProps) {
  const CustomTooltip = ({ active, payload, label }: {
    active?: boolean
    payload?: Array<{ value: number; dataKey: string }>
    label?: string
  }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-ink text-white px-4 py-3 rounded-xl shadow-lg">
          <p className="text-xs text-gray-400 mb-1">{label}</p>
          <p className="text-lg font-semibold font-mono">
            {formatCurrency(payload[0].value)}
          </p>
        </div>
      )
    }
    return null
  }

  if (type === 'bar') {
    return (
      <ResponsiveContainer width="100%" height={height}>
        <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="rgba(226,232,240,0.5)"
            vertical={false}
          />
          <XAxis
            dataKey="name"
            axisLine={false}
            tickLine={false}
            tick={{ fill: '#71717A', fontSize: 12 }}
            dy={10}
          />
          <YAxis
            axisLine={false}
            tickLine={false}
            tick={{ fill: '#71717A', fontSize: 12 }}
            tickFormatter={(v) => `$${v}`}
          />
          <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(226,232,240,0.3)' }} />
          <Bar
            dataKey="positive"
            fill="#10B981"
            radius={[4, 4, 0, 0]}
          />
          <Bar
            dataKey="negative"
            fill="#E11D48"
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    )
  }

  return (
    <ResponsiveContainer width="100%" height={height}>
      <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
        <defs>
          <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#10B981" stopOpacity={0.3} />
            <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid
          strokeDasharray="3 3"
          stroke="rgba(226,232,240,0.5)"
          vertical={false}
        />
        <XAxis
          dataKey="name"
          axisLine={false}
          tickLine={false}
          tick={{ fill: '#71717A', fontSize: 12 }}
          dy={10}
        />
        <YAxis
          axisLine={false}
          tickLine={false}
          tick={{ fill: '#71717A', fontSize: 12 }}
          tickFormatter={(v) => `$${v}`}
        />
        <Tooltip content={<CustomTooltip />} />
        <Area
          type="monotone"
          dataKey="value"
          stroke="#10B981"
          strokeWidth={2}
          fillOpacity={1}
          fill="url(#colorValue)"
        />
      </AreaChart>
    </ResponsiveContainer>
  )
}

interface ProductBreakdownChartProps {
  data: { [key: string]: number }
  height?: number
}

export function ProductBreakdownChart({ data, height = 200 }: ProductBreakdownChartProps) {
  const chartData = Object.entries(data).map(([name, value]) => ({
    name,
    value,
    positive: value >= 0 ? value : 0,
    negative: value < 0 ? Math.abs(value) : 0,
  }))

  return (
    <ResponsiveContainer width="100%" height={height}>
      <BarChart data={chartData} layout="vertical" margin={{ top: 0, right: 10, left: 0, bottom: 0 }}>
        <CartesianGrid
          strokeDasharray="3 3"
          stroke="rgba(226,232,240,0.5)"
          horizontal={false}
        />
        <XAxis
          type="number"
          axisLine={false}
          tickLine={false}
          tick={{ fill: '#71717A', fontSize: 12 }}
          tickFormatter={(v) => `$${v}`}
        />
        <YAxis
          type="category"
          dataKey="name"
          axisLine={false}
          tickLine={false}
          tick={{ fill: '#18181B', fontSize: 12, fontWeight: 500 }}
          width={80}
        />
        <Tooltip
          content={({ active, payload }) => {
            if (active && payload && payload.length) {
              const value = payload[0].payload.value
              return (
                <div className="bg-ink text-white px-4 py-3 rounded-xl shadow-lg">
                  <p className="text-lg font-semibold font-mono">
                    {formatCurrency(value)}
                  </p>
                </div>
              )
            }
            return null
          }}
          cursor={{ fill: 'rgba(226,232,240,0.3)' }}
        />
        <Bar
          dataKey="positive"
          fill="#10B981"
          radius={[0, 4, 4, 0]}
        />
        <Bar
          dataKey="negative"
          fill="#E11D48"
          radius={[0, 4, 4, 0]}
        />
      </BarChart>
    </ResponsiveContainer>
  )
}
