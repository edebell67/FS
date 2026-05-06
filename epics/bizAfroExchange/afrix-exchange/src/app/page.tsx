'use client';

import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { RiskDisclosure } from '@/components/RiskDisclosure';
import { MARKETS, FEATURED_MARKETS } from '@/constants/currencies';
import { ArrowRight, BarChart3, Droplets, Zap } from 'lucide-react';

export default function LandingPage() {
  const featuredMarkets = MARKETS.filter((m) =>
    FEATURED_MARKETS.includes(m.id)
  );

  return (
    <div className="min-h-screen flex flex-col">
      {/* Risk Banner */}
      <RiskDisclosure />

      {/* Header */}
      <header className="border-b">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold bg-gradient-to-r from-green-500 to-emerald-600 bg-clip-text text-transparent">
              AfriX
            </span>
            <Badge variant="outline" className="text-xs">
              SYNTHETIC
            </Badge>
          </div>
          <Link href="/exchange">
            <Button>Enter Exchange</Button>
          </Link>
        </div>
      </header>

      {/* Hero Section */}
      <section className="flex-1 flex items-center">
        <div className="container py-20">
          <div className="max-w-3xl mx-auto text-center space-y-8">
            <Badge variant="secondary" className="text-sm px-4 py-1">
              First Pan-African Currency DEX
            </Badge>

            <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold tracking-tight">
              Trade{' '}
              <span className="bg-gradient-to-r from-green-500 to-emerald-600 bg-clip-text text-transparent">
                Synthetic African FX
              </span>
            </h1>

            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Access African currency markets through synthetic tokens.
              Trade sNGN, sKES, sZAR, sGHS and more with deep liquidity
              and low fees.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link href="/exchange">
                <Button size="lg" className="gap-2 w-full sm:w-auto">
                  View Markets
                  <ArrowRight className="h-4 w-4" />
                </Button>
              </Link>
              <Link href="/etrm-training">
                <Button size="lg" variant="secondary" className="gap-2 w-full sm:w-auto">
                  UK Power Training UI
                </Button>
              </Link>
              <Link href="/liquidity">
                <Button size="lg" variant="outline" className="gap-2 w-full sm:w-auto">
                  <Droplets className="h-4 w-4" />
                  Add Liquidity
                </Button>
              </Link>
            </div>

            <div className="pt-4">
              <RiskDisclosure variant="inline" />
            </div>
          </div>
        </div>
      </section>

      {/* Featured Markets */}
      <section className="border-t bg-muted/30">
        <div className="container py-16">
          <div className="text-center mb-10">
            <h2 className="text-2xl font-bold mb-2">Featured Markets</h2>
            <p className="text-muted-foreground">
              Most active synthetic African currency pairs
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
            {featuredMarkets.map((market) => (
              <Link key={market.id} href={`/exchange?market=${market.id}`}>
                <Card className="hover:border-primary/50 transition-colors cursor-pointer">
                  <CardHeader className="pb-2">
                    <CardTitle className="flex items-center justify-between">
                      <span className="text-lg">{market.symbol}</span>
                      <Badge
                        variant={
                          (market.change24h || 0) >= 0 ? 'default' : 'destructive'
                        }
                        className="text-xs"
                      >
                        {(market.change24h || 0) >= 0 ? '+' : ''}
                        {market.change24h?.toFixed(2)}%
                      </Badge>
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="text-2xl font-mono font-bold">
                          {market.lastPrice?.toFixed(4)}
                        </div>
                        <div className="text-sm text-muted-foreground">
                          {market.base.flagEmoji} {market.base.name} / {market.quote.flagEmoji} {market.quote.name}
                        </div>
                      </div>
                    </div>
                    <div className="mt-3 text-xs text-muted-foreground">
                      24h Volume: {((market.volume24h || 0) / 1000).toFixed(0)}K SETTLE
                    </div>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="border-t">
        <div className="container py-16">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center space-y-3">
              <div className="mx-auto w-12 h-12 rounded-full bg-green-500/10 flex items-center justify-center">
                <BarChart3 className="h-6 w-6 text-green-500" />
              </div>
              <h3 className="font-semibold">Order Book Trading</h3>
              <p className="text-sm text-muted-foreground">
                Traditional limit and market orders with central limit order book matching
              </p>
            </div>
            <div className="text-center space-y-3">
              <div className="mx-auto w-12 h-12 rounded-full bg-blue-500/10 flex items-center justify-center">
                <Droplets className="h-6 w-6 text-blue-500" />
              </div>
              <h3 className="font-semibold">Liquidity Pools</h3>
              <p className="text-sm text-muted-foreground">
                Earn fees by providing liquidity to AMM-style pools
              </p>
            </div>
            <div className="text-center space-y-3">
              <div className="mx-auto w-12 h-12 rounded-full bg-purple-500/10 flex items-center justify-center">
                <Zap className="h-6 w-6 text-purple-500" />
              </div>
              <h3 className="font-semibold">Instant Settlement</h3>
              <p className="text-sm text-muted-foreground">
                All trades settle instantly in SETTLE tokens
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-8">
        <div className="container">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <span className="font-bold text-lg bg-gradient-to-r from-green-500 to-emerald-600 bg-clip-text text-transparent">
                AfriX
              </span>
              <span className="text-sm text-muted-foreground">
                Synthetic African FX Exchange
              </span>
            </div>
            <div className="flex items-center gap-6 text-sm text-muted-foreground">
              <Link href="/exchange" className="hover:text-foreground">
                Exchange
              </Link>
              <Link href="/liquidity" className="hover:text-foreground">
                Liquidity
              </Link>
              <Link href="/portfolio" className="hover:text-foreground">
                Portfolio
              </Link>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
