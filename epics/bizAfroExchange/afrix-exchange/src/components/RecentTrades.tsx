'use client';

import type { Trade } from '@/types';
import { formatDistanceToNow } from 'date-fns';

interface Props {
  trades: Trade[];
}

export function RecentTrades({ trades }: Props) {
  return (
    <div className="h-full flex flex-col text-xs font-mono">
      {/* Header */}
      <div className="flex items-center justify-between px-2 py-1.5 border-b text-muted-foreground">
        <span className="w-1/3">Price</span>
        <span className="w-1/3 text-right">Size</span>
        <span className="w-1/3 text-right">Time</span>
      </div>

      {/* Trades */}
      <div className="flex-1 overflow-auto">
        {trades.map((trade) => (
          <div
            key={trade.id}
            className="flex items-center justify-between px-2 py-0.5 hover:bg-muted/50"
          >
            <span
              className={`w-1/3 ${
                trade.side === 'buy' ? 'text-green-500' : 'text-red-500'
              }`}
            >
              {trade.price.toFixed(6)}
            </span>
            <span className="w-1/3 text-right">{trade.size.toLocaleString()}</span>
            <span className="w-1/3 text-right text-muted-foreground">
              {formatDistanceToNow(trade.timestamp, { addSuffix: false })}
            </span>
          </div>
        ))}

        {trades.length === 0 && (
          <div className="p-4 text-center text-muted-foreground">
            No recent trades
          </div>
        )}
      </div>
    </div>
  );
}
