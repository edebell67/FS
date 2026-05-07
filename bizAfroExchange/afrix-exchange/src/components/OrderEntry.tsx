'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { useExchangeStore } from '@/store/useExchangeStore';
import type { Market, OrderSide, OrderType } from '@/types';

interface Props {
  market: Market | null;
  selectedPrice?: number;
}

export function OrderEntry({ market, selectedPrice }: Props) {
  const [orderType, setOrderType] = useState<OrderType>('limit');
  const [side, setSide] = useState<OrderSide>('buy');
  const [price, setPrice] = useState(selectedPrice?.toString() || '');
  const [amount, setAmount] = useState('');

  const addOrder = useExchangeStore((state) => state.addOrder);

  // Update price when selected from order book
  useState(() => {
    if (selectedPrice) {
      setPrice(selectedPrice.toString());
    }
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!market) return;

    const order = {
      id: `order_${Date.now()}`,
      market: market.symbol,
      side,
      type: orderType,
      price: orderType === 'limit' ? parseFloat(price) : undefined,
      size: parseFloat(amount),
      filled: 0,
      status: 'open' as const,
      timestamp: Date.now(),
    };

    addOrder(order);

    // Reset form
    setAmount('');
    if (orderType === 'market') {
      setPrice('');
    }
  };

  const total = price && amount ? parseFloat(price) * parseFloat(amount) : 0;

  return (
    <div className="p-4 space-y-4">
      <Tabs value={orderType} onValueChange={(v) => setOrderType(v as OrderType)}>
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="limit">Limit</TabsTrigger>
          <TabsTrigger value="market">Market</TabsTrigger>
        </TabsList>

        <TabsContent value="limit" className="space-y-4 mt-4">
          <div className="grid grid-cols-2 gap-2">
            <Button
              type="button"
              variant={side === 'buy' ? 'default' : 'outline'}
              className={side === 'buy' ? 'bg-green-600 hover:bg-green-700' : ''}
              onClick={() => setSide('buy')}
            >
              Buy
            </Button>
            <Button
              type="button"
              variant={side === 'sell' ? 'default' : 'outline'}
              className={side === 'sell' ? 'bg-red-600 hover:bg-red-700' : ''}
              onClick={() => setSide('sell')}
            >
              Sell
            </Button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="price">Price ({market?.quote.syntheticSymbol || 'Quote'})</Label>
              <Input
                id="price"
                type="number"
                step="any"
                placeholder="0.00"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="amount">Amount ({market?.base.syntheticSymbol || 'Base'})</Label>
              <Input
                id="amount"
                type="number"
                step="any"
                placeholder="0.00"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
              />
            </div>

            <div className="flex items-center justify-between text-sm text-muted-foreground">
              <span>Total</span>
              <span className="font-mono">
                {total.toFixed(4)} {market?.quote.syntheticSymbol || 'Quote'}
              </span>
            </div>

            <Button
              type="submit"
              className={`w-full ${
                side === 'buy'
                  ? 'bg-green-600 hover:bg-green-700'
                  : 'bg-red-600 hover:bg-red-700'
              }`}
              disabled={!market || !price || !amount}
            >
              {side === 'buy' ? 'Buy' : 'Sell'} {market?.base.syntheticSymbol || 'Base'}
            </Button>
          </form>
        </TabsContent>

        <TabsContent value="market" className="space-y-4 mt-4">
          <div className="grid grid-cols-2 gap-2">
            <Button
              type="button"
              variant={side === 'buy' ? 'default' : 'outline'}
              className={side === 'buy' ? 'bg-green-600 hover:bg-green-700' : ''}
              onClick={() => setSide('buy')}
            >
              Buy
            </Button>
            <Button
              type="button"
              variant={side === 'sell' ? 'default' : 'outline'}
              className={side === 'sell' ? 'bg-red-600 hover:bg-red-700' : ''}
              onClick={() => setSide('sell')}
            >
              Sell
            </Button>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="market-amount">Amount ({market?.base.syntheticSymbol || 'Base'})</Label>
              <Input
                id="market-amount"
                type="number"
                step="any"
                placeholder="0.00"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                required
              />
            </div>

            <div className="text-sm text-muted-foreground">
              Market orders execute at the best available price
            </div>

            <Button
              type="submit"
              className={`w-full ${
                side === 'buy'
                  ? 'bg-green-600 hover:bg-green-700'
                  : 'bg-red-600 hover:bg-red-700'
              }`}
              disabled={!market || !amount}
            >
              {side === 'buy' ? 'Buy' : 'Sell'} {market?.base.syntheticSymbol || 'Base'}
            </Button>
          </form>
        </TabsContent>
      </Tabs>

      <div className="text-xs text-muted-foreground text-center">
        Maker fee: {((market?.makerFee || 0) * 100).toFixed(2)}% | Taker fee: {((market?.takerFee || 0) * 100).toFixed(2)}%
      </div>
    </div>
  );
}
