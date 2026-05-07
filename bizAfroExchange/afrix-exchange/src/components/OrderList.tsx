'use client';

import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { useExchangeStore } from '@/store/useExchangeStore';
import { X } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

export function OrderList() {
  const { orders, cancelOrder } = useExchangeStore();

  const activeOrders = orders.filter(
    (o) => o.status === 'open' || o.status === 'partial'
  );

  if (activeOrders.length === 0) {
    return (
      <div className="h-full flex items-center justify-center text-sm text-muted-foreground">
        No open orders
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
            <th className="text-right p-2 font-medium">Price</th>
            <th className="text-right p-2 font-medium">Size</th>
            <th className="text-right p-2 font-medium">Filled</th>
            <th className="text-right p-2 font-medium">Time</th>
            <th className="text-right p-2 font-medium"></th>
          </tr>
        </thead>
        <tbody>
          {activeOrders.map((order) => (
            <tr key={order.id} className="border-b hover:bg-muted/50">
              <td className="p-2 font-medium">{order.market}</td>
              <td className="p-2">
                <Badge
                  variant={order.side === 'buy' ? 'default' : 'destructive'}
                  className="text-[10px] px-1.5"
                >
                  {order.side.toUpperCase()}
                </Badge>
              </td>
              <td className="p-2 text-right font-mono">
                {order.type === 'market' ? 'Market' : order.price?.toFixed(6)}
              </td>
              <td className="p-2 text-right font-mono">
                {order.size.toLocaleString()}
              </td>
              <td className="p-2 text-right font-mono">
                {order.filled.toLocaleString()}
              </td>
              <td className="p-2 text-right text-muted-foreground">
                {formatDistanceToNow(order.timestamp, { addSuffix: true })}
              </td>
              <td className="p-2 text-right">
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-6 w-6 p-0"
                  onClick={() => cancelOrder(order.id)}
                >
                  <X className="h-3 w-3" />
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
