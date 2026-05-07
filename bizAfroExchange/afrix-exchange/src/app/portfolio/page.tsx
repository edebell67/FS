'use client';

import { useEffect, useState } from 'react';
import { Navbar } from '@/components/Navbar';
import { RiskDisclosure } from '@/components/RiskDisclosure';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { useExchangeStore } from '@/store/useExchangeStore';
import { mockAPI } from '@/lib/api/mock';
import type { Wallet } from '@/types';
import { formatDistanceToNow } from 'date-fns';

export default function PortfolioPage() {
  const [wallet, setWallet] = useState<Wallet | null>(null);
  const { orders, positions } = useExchangeStore();

  useEffect(() => {
    const loadWallet = async () => {
      const data = await mockAPI.getWallet();
      setWallet(data);
    };
    loadWallet();
  }, []);

  const allOrders = orders.slice().sort((a, b) => b.timestamp - a.timestamp);

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <RiskDisclosure />
      <Navbar />

      <div className="container py-8">
        {/* Portfolio Value */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Portfolio Value</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold font-mono">
              {wallet?.totalValue.toLocaleString() || '---'}{' '}
              <span className="text-lg text-muted-foreground">SETTLE</span>
            </div>
          </CardContent>
        </Card>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Balances */}
          <Card className="lg:col-span-1">
            <CardHeader>
              <CardTitle>Balances</CardTitle>
            </CardHeader>
            <CardContent>
              {wallet ? (
                <div className="space-y-3">
                  {Object.entries(wallet.balances).map(([currency, amount]) => (
                    <div
                      key={currency}
                      className="flex items-center justify-between py-2 border-b last:border-0"
                    >
                      <div className="flex items-center gap-2">
                        <Badge variant={currency === 'SETTLE' ? 'default' : 'outline'}>
                          {currency}
                        </Badge>
                      </div>
                      <span className="font-mono">
                        {amount.toLocaleString()}
                      </span>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-muted-foreground">Loading...</div>
              )}
            </CardContent>
          </Card>

          {/* Open Positions */}
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle>Open Positions</CardTitle>
            </CardHeader>
            <CardContent>
              {positions.length > 0 ? (
                <div className="overflow-auto">
                  <table className="w-full text-sm">
                    <thead>
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
                        <tr key={index} className="border-b">
                          <td className="p-2 font-medium">{position.market}</td>
                          <td className="p-2">
                            <Badge
                              variant={position.side === 'long' ? 'default' : 'destructive'}
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
                              position.unrealizedPnL >= 0
                                ? 'text-green-500'
                                : 'text-red-500'
                            }`}
                          >
                            {position.unrealizedPnL >= 0 ? '+' : ''}
                            {position.unrealizedPnL.toFixed(2)} (
                            {position.unrealizedPnLPercent >= 0 ? '+' : ''}
                            {position.unrealizedPnLPercent.toFixed(2)}%)
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="text-center py-8 text-muted-foreground">
                  No open positions
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Activity History */}
        <Card className="mt-8">
          <CardHeader>
            <CardTitle>Activity History</CardTitle>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="trades">
              <TabsList>
                <TabsTrigger value="trades">Trades</TabsTrigger>
                <TabsTrigger value="orders">Orders</TabsTrigger>
                <TabsTrigger value="liquidity">Liquidity</TabsTrigger>
              </TabsList>

              <TabsContent value="trades" className="mt-4">
                <div className="text-center py-8 text-muted-foreground">
                  No trade history yet
                </div>
              </TabsContent>

              <TabsContent value="orders" className="mt-4">
                {allOrders.length > 0 ? (
                  <div className="overflow-auto">
                    <table className="w-full text-sm">
                      <thead>
                        <tr className="border-b text-muted-foreground">
                          <th className="text-left p-2 font-medium">Market</th>
                          <th className="text-left p-2 font-medium">Type</th>
                          <th className="text-left p-2 font-medium">Side</th>
                          <th className="text-right p-2 font-medium">Price</th>
                          <th className="text-right p-2 font-medium">Size</th>
                          <th className="text-left p-2 font-medium">Status</th>
                          <th className="text-right p-2 font-medium">Time</th>
                        </tr>
                      </thead>
                      <tbody>
                        {allOrders.map((order) => (
                          <tr key={order.id} className="border-b">
                            <td className="p-2 font-medium">{order.market}</td>
                            <td className="p-2">
                              <Badge variant="outline">{order.type.toUpperCase()}</Badge>
                            </td>
                            <td className="p-2">
                              <Badge
                                variant={order.side === 'buy' ? 'default' : 'destructive'}
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
                            <td className="p-2">
                              <Badge
                                variant={
                                  order.status === 'filled'
                                    ? 'default'
                                    : order.status === 'cancelled'
                                    ? 'secondary'
                                    : 'outline'
                                }
                              >
                                {order.status.toUpperCase()}
                              </Badge>
                            </td>
                            <td className="p-2 text-right text-muted-foreground">
                              {formatDistanceToNow(order.timestamp, { addSuffix: true })}
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    No order history yet
                  </div>
                )}
              </TabsContent>

              <TabsContent value="liquidity" className="mt-4">
                <div className="text-center py-8 text-muted-foreground">
                  No liquidity history yet
                </div>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
