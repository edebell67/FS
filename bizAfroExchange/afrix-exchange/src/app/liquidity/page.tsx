'use client';

import { useEffect, useState } from 'react';
import { Navbar } from '@/components/Navbar';
import { RiskDisclosure } from '@/components/RiskDisclosure';
import { PoolCard } from '@/components/PoolCard';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { mockAPI } from '@/lib/api/mock';
import { useLiquidityStore } from '@/store/useLiquidityStore';
// Types are inferred from store
import { Info, Plus } from 'lucide-react';

export default function LiquidityPage() {
  const { pools, setPools, userPositions, setUserPositions } = useLiquidityStore();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      const [poolsData, positionsData] = await Promise.all([
        mockAPI.getPools(),
        mockAPI.getLiquidityPositions(),
      ]);
      setPools(poolsData);
      setUserPositions(positionsData);
      setIsLoading(false);
    };
    loadData();
  }, [setPools, setUserPositions]);

  const totalValue = userPositions.reduce((sum, p) => sum + p.value, 0);
  const totalFees = userPositions.reduce((sum, p) => sum + p.unclaimedFees, 0);

  return (
    <div className="min-h-screen flex flex-col bg-background">
      <RiskDisclosure />
      <Navbar />

      <div className="container py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-2xl font-bold">Liquidity Pools</h1>
            <p className="text-muted-foreground flex items-center gap-2 mt-1">
              <Info className="h-4 w-4" />
              Optional AMM pools - complement order book, don&apos;t replace it
            </p>
          </div>
          <Button className="gap-2">
            <Plus className="h-4 w-4" />
            Create Pool
          </Button>
        </div>

        {/* User Positions Summary */}
        {userPositions.length > 0 && (
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="text-lg">Your Liquidity</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <div className="text-sm text-muted-foreground">Total Value</div>
                  <div className="text-2xl font-bold font-mono">
                    {totalValue.toLocaleString()} <span className="text-sm text-muted-foreground">SETTLE</span>
                  </div>
                </div>
                <div>
                  <div className="text-sm text-muted-foreground">Unclaimed Fees</div>
                  <div className="text-2xl font-bold font-mono text-green-500">
                    +{totalFees.toFixed(2)} <span className="text-sm text-muted-foreground">SETTLE</span>
                  </div>
                </div>
                <div>
                  <div className="text-sm text-muted-foreground">Active Positions</div>
                  <div className="text-2xl font-bold">{userPositions.length}</div>
                </div>
              </div>

              <div className="mt-6 space-y-2">
                {userPositions.map((position) => {
                  const pool = pools.find((p) => p.id === position.poolId);
                  return (
                    <div
                      key={position.poolId}
                      className="flex items-center justify-between p-3 rounded-lg bg-muted/50"
                    >
                      <div className="flex items-center gap-3">
                        <span className="font-medium">{pool?.pair || position.poolId}</span>
                        <Badge variant="outline" className="text-xs">
                          {(position.share * 100).toFixed(2)}% share
                        </Badge>
                      </div>
                      <div className="flex items-center gap-6 text-sm">
                        <div>
                          <span className="text-muted-foreground">Value: </span>
                          <span className="font-mono">{position.value.toFixed(2)} SETTLE</span>
                        </div>
                        <div>
                          <span className="text-muted-foreground">Fees: </span>
                          <span className="font-mono text-green-500">+{position.unclaimedFees.toFixed(2)}</span>
                        </div>
                        <Button size="sm" variant="outline">
                          Manage
                        </Button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        )}

        {/* Pool List */}
        <div className="mb-4">
          <h2 className="text-lg font-semibold">All Pools</h2>
        </div>

        {isLoading ? (
          <div className="text-center py-12 text-muted-foreground">
            Loading pools...
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {pools.map((pool) => (
              <PoolCard key={pool.id} pool={pool} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
