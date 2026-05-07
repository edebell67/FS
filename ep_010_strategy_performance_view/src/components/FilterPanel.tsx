'use client'

import { Search, Filter, X, RotateCcw } from 'lucide-react'
import { useStore } from '@/hooks/useStore'
import { cn } from '@/lib/utils'

interface FilterPanelProps {
  products: string[]
}

export function FilterPanel({ products }: FilterPanelProps) {
  const { filters, setFilter, resetFilters } = useStore()

  const hasActiveFilters =
    filters.strategy ||
    filters.product ||
    filters.minNet !== null ||
    filters.maxNet !== null ||
    filters.pickNowOnly

  return (
    <div className="card-compact mb-6">
      <div className="flex flex-col md:flex-row md:items-center gap-4">
        <div className="flex-1">
          <div className="relative">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted" />
            <input
              type="text"
              value={filters.strategy}
              onChange={(e) => setFilter('strategy', e.target.value)}
              placeholder="Search strategies..."
              className="input-field pl-12"
            />
            {filters.strategy && (
              <button
                onClick={() => setFilter('strategy', '')}
                className="absolute right-4 top-1/2 -translate-y-1/2 text-muted hover:text-steel"
              >
                <X className="w-4 h-4" />
              </button>
            )}
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <select
            value={filters.product}
            onChange={(e) => setFilter('product', e.target.value)}
            className="input-field w-full md:w-auto md:min-w-[160px] appearance-none bg-[url('data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%22292.4%22%20height%3D%22292.4%22%3E%3Cpath%20fill%3D%22%2371717A%22%20d%3D%22M287%2069.4a17.6%2017.6%200%200%200-13-5.4H18.4c-5%200-9.3%201.8-12.9%205.4A17.6%2017.6%200%200%200%200%2082.2c0%205%201.8%209.3%205.4%2012.9l128%20127.9c3.6%203.6%207.8%205.4%2012.8%205.4s9.2-1.8%2012.8-5.4L287%2095c3.5-3.5%205.4-7.8%205.4-12.8%200-5-1.9-9.2-5.5-12.8z%22%2F%3E%3C%2Fsvg%3E')] bg-[length:12px] bg-[right_16px_center] bg-no-repeat pr-10"
          >
            <option value="">All Products</option>
            {products.map((product) => (
              <option key={product} value={product}>
                {product}
              </option>
            ))}
          </select>

          <div className="flex items-center gap-2">
            <input
              type="number"
              value={filters.minNet ?? ''}
              onChange={(e) => setFilter('minNet', e.target.value ? Number(e.target.value) : null)}
              placeholder="Min Net"
              className="input-field w-24 md:w-28 text-sm"
            />
            <span className="text-muted">to</span>
            <input
              type="number"
              value={filters.maxNet ?? ''}
              onChange={(e) => setFilter('maxNet', e.target.value ? Number(e.target.value) : null)}
              placeholder="Max Net"
              className="input-field w-24 md:w-28 text-sm"
            />
          </div>

          <label className="flex items-center gap-2 cursor-pointer select-none">
            <input
              type="checkbox"
              checked={filters.pickNowOnly}
              onChange={(e) => setFilter('pickNowOnly', e.target.checked)}
              className="w-4 h-4 rounded border-whisper text-electric focus:ring-electric"
            />
            <span className="text-sm text-steel">Active Picks Only</span>
          </label>

          {hasActiveFilters && (
            <button
              onClick={resetFilters}
              className="flex items-center gap-2 text-sm text-steel hover:text-ink transition-colors"
            >
              <RotateCcw className="w-4 h-4" />
              <span className="hidden md:inline">Reset</span>
            </button>
          )}
        </div>
      </div>

      {hasActiveFilters && (
        <div className="flex flex-wrap items-center gap-2 mt-4 pt-4 border-t border-whisper">
          <Filter className="w-4 h-4 text-muted" />
          <span className="text-xs text-muted uppercase tracking-wider mr-2">Active Filters:</span>

          {filters.strategy && (
            <FilterTag
              label={`Strategy: ${filters.strategy}`}
              onRemove={() => setFilter('strategy', '')}
            />
          )}
          {filters.product && (
            <FilterTag
              label={`Product: ${filters.product}`}
              onRemove={() => setFilter('product', '')}
            />
          )}
          {filters.minNet !== null && (
            <FilterTag
              label={`Min: $${filters.minNet}`}
              onRemove={() => setFilter('minNet', null)}
            />
          )}
          {filters.maxNet !== null && (
            <FilterTag
              label={`Max: $${filters.maxNet}`}
              onRemove={() => setFilter('maxNet', null)}
            />
          )}
          {filters.pickNowOnly && (
            <FilterTag
              label="Active Picks"
              onRemove={() => setFilter('pickNowOnly', false)}
            />
          )}
        </div>
      )}
    </div>
  )
}

function FilterTag({ label, onRemove }: { label: string; onRemove: () => void }) {
  return (
    <span className="inline-flex items-center gap-1 px-3 py-1 bg-gray-100 rounded-full text-xs font-medium text-ink">
      {label}
      <button
        onClick={onRemove}
        className="ml-1 p-0.5 hover:bg-gray-200 rounded-full transition-colors"
      >
        <X className="w-3 h-3" />
      </button>
    </span>
  )
}
