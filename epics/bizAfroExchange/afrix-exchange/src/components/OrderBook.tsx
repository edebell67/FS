'use client';

import { useMemo } from 'react';
import type { OrderBook as OrderBookType } from '@/types';

interface Props {
  orderBook: OrderBookType | null;
  onPriceClick?: (price: number) => void;
}

export function OrderBook({ orderBook, onPriceClick }: Props) {
  const { bids, asks, maxTotal } = useMemo(() => {
    if (!orderBook) return { bids: [], asks: [], maxTotal: 0 };

    const bids = orderBook.bids.slice(0, 12);
    const asks = orderBook.asks.slice(0, 12).reverse();

    const maxBidTotal = bids[bids.length - 1]?.total || 0;
    const maxAskTotal = asks[0]?.total || 0;
    const maxTotal = Math.max(maxBidTotal, maxAskTotal);

    return { bids, asks, maxTotal };
  }, [orderBook]);

  if (!orderBook) {
    return (
      <div className="h-full flex items-center justify-center text-muted-foreground">
        Loading order book...
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col text-xs font-mono">
      {/* Header */}
      <div className="flex items-center justify-between px-2 py-1.5 border-b text-muted-foreground">
        <span className="w-1/3">Price</span>
        <span className="w-1/3 text-right">Size</span>
        <span className="w-1/3 text-right">Total</span>
      </div>

      {/* Asks (sells) - reversed so lowest ask is at bottom */}
      <div className="flex-1 overflow-hidden flex flex-col">
        <div className="flex-1 overflow-auto flex flex-col justify-end">
          {asks.map((level, i) => (
            <div
              key={`ask-${i}`}
              className="relative flex items-center justify-between px-2 py-0.5 hover:bg-muted/50 cursor-pointer"
              onClick={() => onPriceClick?.(level.price)}
            >
              <div
                className="absolute inset-y-0 right-0 bg-red-500/10"
                style={{ width: `${((level.total || 0) / maxTotal) * 100}%` }}
              />
              <span className="relative w-1/3 text-red-500">
                {level.price.toFixed(6)}
              </span>
              <span className="relative w-1/3 text-right">
                {level.size.toLocaleString()}
              </span>
              <span className="relative w-1/3 text-right text-muted-foreground">
                {(level.total || 0).toLocaleString()}
              </span>
            </div>
          ))}
        </div>

        {/* Spread */}
        <div className="px-2 py-1.5 border-y bg-muted/30 text-center">
          <span className="text-muted-foreground">Spread: </span>
          <span className="text-foreground">
            {orderBook.spread.toFixed(6)} ({((orderBook.spread / (orderBook.asks[0]?.price || 1)) * 100).toFixed(3)}%)
          </span>
        </div>

        {/* Bids (buys) */}
        <div className="flex-1 overflow-auto">
          {bids.map((level, i) => (
            <div
              key={`bid-${i}`}
              className="relative flex items-center justify-between px-2 py-0.5 hover:bg-muted/50 cursor-pointer"
              onClick={() => onPriceClick?.(level.price)}
            >
              <div
                className="absolute inset-y-0 right-0 bg-green-500/10"
                style={{ width: `${((level.total || 0) / maxTotal) * 100}%` }}
              />
              <span className="relative w-1/3 text-green-500">
                {level.price.toFixed(6)}
              </span>
              <span className="relative w-1/3 text-right">
                {level.size.toLocaleString()}
              </span>
              <span className="relative w-1/3 text-right text-muted-foreground">
                {(level.total || 0).toLocaleString()}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
