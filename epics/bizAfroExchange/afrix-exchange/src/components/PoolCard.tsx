'use client';

import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import type { Pool } from '@/types';

interface Props {
  pool: Pool;
}

export function PoolCard({ pool }: Props) {
  return (
    <Link href={`/liquidity/${pool.id}`}>
      <Card className="hover:border-primary/50 transition-colors cursor-pointer">
        <CardHeader className="pb-2">
          <CardTitle className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-lg">{pool.pair}</span>
              <Badge variant="outline" className="text-[10px]">
                {(pool.feeTier * 100).toFixed(1)}%
              </Badge>
            </div>
            <Badge variant="secondary" className="text-xs">
              {(pool.apr * 100).toFixed(1)}% APR
            </Badge>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-3 gap-4 text-sm">
            <div>
              <div className="text-muted-foreground text-xs">TVL</div>
              <div className="font-mono font-medium">
                {(pool.tvl / 1000).toFixed(0)}K
              </div>
            </div>
            <div>
              <div className="text-muted-foreground text-xs">Volume 24h</div>
              <div className="font-mono font-medium">
                {(pool.volume24h / 1000).toFixed(0)}K
              </div>
            </div>
            <div>
              <div className="text-muted-foreground text-xs">Price</div>
              <div className="font-mono font-medium">
                {pool.price.toFixed(4)}
              </div>
            </div>
          </div>
          <div className="mt-3 text-xs text-muted-foreground">
            {pool.base.flagEmoji} {pool.base.syntheticSymbol} / {pool.quote.flagEmoji} {pool.quote.syntheticSymbol}
          </div>
        </CardContent>
      </Card>
    </Link>
  );
}
