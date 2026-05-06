'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { Navbar } from '@/components/Navbar';
import { RiskDisclosure } from '@/components/RiskDisclosure';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { mockAPI } from '@/lib/api/mock';
import type { Pool } from '@/types';
import { ArrowLeft, AlertTriangle } from 'lucide-react';

export default function PoolDetailPage() {
  const params = useParams();
  const poolId = params.poolId as string;

  const [pool, setPool] = useState<Pool | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [amount0, setAmount0] = useState('');
  const [amount1, setAmount1] = useState('');
  const [provideToOrderBook, setProvideToOrderBook] = useState(false);

  useEffect(() => {
    const loadPool = async () => {
      const data = await mockAPI.getPool(poolId);
      setPool(data || null);
      setIsLoading(false);
    };
    loadPool();
  }, [poolId]);

  // Calculate paired amount when one changes
  const handleAmount0Change = (value: string) => {
    setAmount0(value);
    if (pool && value) {
      const amount = parseFloat(value);
      setAmount1((amount * pool.price).toFixed(4));
    } else {
      setAmount1('');
    }
  };

  const handleAmount1Change = (value: string) => {
    setAmount1(value);
    if (pool && value) {
      const amount = parseFloat(value);
      setAmount0((amount / pool.price).toFixed(4));
    } else {
      setAmount0('');
    }
  };

  // Calculate LP tokens to receive
  const lpTokensToReceive = pool && amount0 && amount1
    ? (parseFloat(amount0) / pool.reserve0) * pool.lpTotalSupply
    : 0;

  if (isLoading) {
    return (
      <div className="min-h-screen flex flex-col bg-background">
        <RiskDisclosure />
        <Navbar />
        <div className="flex-1 flex items-center justify-center">
          Loading pool...
        </div>
      </div>
    );
  }

  if (!pool) {
    return (
      <div className="min-h-screen flex flex-col bg-background">
        <RiskDisclosure />
        <Navbar />
        <div className="flex-1 flex items-center justify-center">
          Pool not found
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <RiskDisclosure />
      <Navbar />

      <div className="container py-8 max-w-4xl">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Link href="/liquidity">
            <Button variant="ghost" size="sm" className="gap-2">
              <ArrowLeft className="h-4 w-4" />
              Back
            </Button>
          </Link>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold">{pool.pair} Pool</h1>
              <Badge variant="outline">{(pool.feeTier * 100).toFixed(1)}% fee</Badge>
            </div>
            <p className="text-muted-foreground text-sm">
              {pool.base.flagEmoji} {pool.base.name} / {pool.quote.flagEmoji} {pool.quote.name}
            </p>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <Card>
            <CardContent className="pt-6">
              <div className="text-sm text-muted-foreground">TVL</div>
              <div className="text-2xl font-bold font-mono">
                {(pool.tvl / 1000).toFixed(0)}K
              </div>
              <div className="text-xs text-muted-foreground">SETTLE</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-sm text-muted-foreground">APR</div>
              <div className="text-2xl font-bold font-mono text-green-500">
                {(pool.apr * 100).toFixed(1)}%
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-sm text-muted-foreground">Volume 24h</div>
              <div className="text-2xl font-bold font-mono">
                {(pool.volume24h / 1000).toFixed(0)}K
              </div>
              <div className="text-xs text-muted-foreground">SETTLE</div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-sm text-muted-foreground">Price</div>
              <div className="text-2xl font-bold font-mono">
                {pool.price.toFixed(4)}
              </div>
              <div className="text-xs text-muted-foreground">{pool.quote.syntheticSymbol}/{pool.base.syntheticSymbol}</div>
            </CardContent>
          </Card>
        </div>

        {/* Your Position (mock) */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Your Position</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-3 gap-4 text-sm">
              <div>
                <div className="text-muted-foreground">Your Liquidity</div>
                <div className="text-lg font-bold font-mono">5,000.00 <span className="text-xs text-muted-foreground">SETTLE</span></div>
              </div>
              <div>
                <div className="text-muted-foreground">Pool Share</div>
                <div className="text-lg font-bold font-mono">0.4%</div>
              </div>
              <div>
                <div className="text-muted-foreground">Unclaimed Fees</div>
                <div className="text-lg font-bold font-mono text-green-500">+12.34 <span className="text-xs text-muted-foreground">SETTLE</span></div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Add/Remove Liquidity */}
        <Card>
          <Tabs defaultValue="add">
            <CardHeader className="pb-0">
              <TabsList>
                <TabsTrigger value="add">Add Liquidity</TabsTrigger>
                <TabsTrigger value="remove">Remove Liquidity</TabsTrigger>
              </TabsList>
            </CardHeader>
            <CardContent className="pt-6">
              <TabsContent value="add" className="space-y-6 mt-0">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label>Amount {pool.base.syntheticSymbol}</Label>
                    <Input
                      type="number"
                      placeholder="0.00"
                      value={amount0}
                      onChange={(e) => handleAmount0Change(e.target.value)}
                    />
                    <div className="text-xs text-muted-foreground">
                      Balance: 1,245,000 {pool.base.syntheticSymbol}
                    </div>
                  </div>
                  <div className="space-y-2">
                    <Label>Amount {pool.quote.syntheticSymbol} (balanced)</Label>
                    <Input
                      type="number"
                      placeholder="0.00"
                      value={amount1}
                      onChange={(e) => handleAmount1Change(e.target.value)}
                    />
                    <div className="text-xs text-muted-foreground">
                      Balance: 832,000 {pool.quote.syntheticSymbol}
                    </div>
                  </div>
                </div>

                <div className="p-4 rounded-lg bg-muted/50 space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">You will receive</span>
                    <span className="font-mono font-medium">{lpTokensToReceive.toFixed(2)} LP tokens</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">Share of pool</span>
                    <span className="font-mono">{pool.lpTotalSupply > 0 ? ((lpTokensToReceive / (pool.lpTotalSupply + lpTokensToReceive)) * 100).toFixed(4) : 0}%</span>
                  </div>
                </div>

                <div className="flex items-center justify-between p-4 rounded-lg border">
                  <div>
                    <div className="font-medium">Also provide to order book</div>
                    <div className="text-sm text-muted-foreground">Experimental market maker mode</div>
                  </div>
                  <Switch
                    checked={provideToOrderBook}
                    onCheckedChange={setProvideToOrderBook}
                  />
                </div>

                <div className="flex items-start gap-2 p-4 rounded-lg bg-yellow-500/10 border border-yellow-500/20">
                  <AlertTriangle className="h-5 w-5 text-yellow-500 flex-shrink-0 mt-0.5" />
                  <div className="text-sm text-yellow-600 dark:text-yellow-400">
                    <strong>Impermanent Loss Risk:</strong> Providing liquidity exposes you to impermanent loss if the relative price of the tokens changes significantly.
                  </div>
                </div>

                <Button className="w-full" size="lg" disabled={!amount0 || !amount1}>
                  Add Liquidity
                </Button>
              </TabsContent>

              <TabsContent value="remove" className="space-y-6 mt-0">
                <div className="space-y-2">
                  <Label>Amount to remove</Label>
                  <div className="flex gap-2">
                    {[25, 50, 75, 100].map((pct) => (
                      <Button key={pct} variant="outline" size="sm" className="flex-1">
                        {pct}%
                      </Button>
                    ))}
                  </div>
                </div>

                <div className="p-4 rounded-lg bg-muted/50 space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-muted-foreground">You will receive</span>
                    <div className="text-right">
                      <div className="font-mono">~12,500 {pool.base.syntheticSymbol}</div>
                      <div className="font-mono">~3,570 {pool.quote.syntheticSymbol}</div>
                    </div>
                  </div>
                </div>

                <Button className="w-full" size="lg" variant="destructive">
                  Remove Liquidity
                </Button>
              </TabsContent>
            </CardContent>
          </Tabs>
        </Card>
      </div>
    </div>
  );
}
