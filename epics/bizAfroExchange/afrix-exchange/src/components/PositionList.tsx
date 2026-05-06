'use client';

import { Badge } from '@/components/ui/badge';
import { useExchangeStore } from '@/store/useExchangeStore';

export function PositionList() {
  const positions = useExchangeStore((state) => state.positions);

  if (positions.length === 0) {
    return (
      <div className="h-full flex items-center justify-center text-sm text-muted-foreground">
        No open positions
      </div>
    );
  }

  return (
    <div className="h-full overflow-auto">
      <table className="w-full text-xs">
        <thead className="sticky top-0 bg-background">
          <tr className="border-b text-muted-foreground">
            <th className="text-left p-2 font-medium">Market</th>
            <th className="text-left p-2 font-medium">Side</th>
            <th className="text-right p-2 font-medium">Size</th>
            <th className="text-right p-2 font-medium">Entry</th>
            <th className="text-right p-2 font-medium">Current</th>
            <th className="text-right p-2 font-medium">PnL</th>
          </tr>
        </thead>
        <tbody>
          {positions.map((position, index) => (
            <tr key={index} className="border-b hover:bg-muted/50">
              <td className="p-2 font-medium">{position.market}</td>
              <td className="p-2">
                <Badge
                  variant={position.side === 'long' ? 'default' : 'destructive'}
                  className="text-[10px] px-1.5"
                >
                  {position.side.toUpperCase()}
                </Badge>
              </td>
              <td className="p-2 text-right font-mono">
                {position.size.toLocaleString()}
              </td>
              <td className="p-2 text-right font-mono">
                {position.avgEntryPrice.toFixed(4)}
              </td>
              <td className="p-2 text-right font-mono">
                {position.currentPrice.toFixed(4)}
              </td>
              <td
                className={`p-2 text-right font-mono ${
                  position.unrealizedPnL >= 0 ? 'text-green-500' : 'text-red-500'
                }`}
              >
                {position.unrealizedPnL >= 0 ? '+' : ''}
                {position.unrealizedPnL.toFixed(2)} ({position.unrealizedPnLPercent >= 0 ? '+' : ''}
                {position.unrealizedPnLPercent.toFixed(2)}%)
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
