'use client';

import { Suspense, useEffect, useState, useCallback } from 'react';
import { useSearchParams } from 'next/navigation';
import { Navbar } from '@/components/Navbar';
import { RiskDisclosure } from '@/components/RiskDisclosure';
import { TradingViewChart } from '@/components/TradingViewChart';
import { OrderBook } from '@/components/OrderBook';
import { OrderEntry } from '@/components/OrderEntry';
import { MarketSelector } from '@/components/MarketSelector';
import { RecentTrades } from '@/components/RecentTrades';
import { OrderList } from '@/components/OrderList';
import { PositionList } from '@/components/PositionList';
import { Card } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { useExchangeStore } from '@/store/useExchangeStore';
import { mockAPI } from '@/lib/api/mock';
import { connectMarketStream } from '@/lib/ws/mockWebSocket';
import { MARKETS } from '@/constants/currencies';
import type { Market, CandlestickData } from '@/types';

function ExchangeContent() {
  const searchParams = useSearchParams();
  const marketParam = searchParams.get('market');

  const { selectedMarket, setSelectedMarket, setOrderBook, orderBook, recentTrades, setRecentTrades } = useExchangeStore();

  const [chartData, setChartData] = useState<CandlestickData[]>([]);
  const [chartInterval, setChartInterval] = useState('1h');
  const [selectedPrice, setSelectedPrice] = useState<number | undefined>();

  // Initialize market from URL or default
  useEffect(() => {
    const market = marketParam
      ? MARKETS.find((m) => m.id === marketParam)
      : MARKETS[0];
    if (market) {
      setSelectedMarket(market);
    }
  }, [marketParam, setSelectedMarket]);

  // Load chart data
  const loadChartData = useCallback(async () => {
    if (!selectedMarket) return;
    const data = await mockAPI.getCandlestickData(selectedMarket.id, chartInterval);
    setChartData(data);
  }, [selectedMarket, chartInterval]);

  // Load order book
  // Initial data load
  useEffect(() => {
    loadChartData();
  }, [loadChartData]);

  // Simulated WebSocket market stream
  useEffect(() => {
    if (!selectedMarket) return;
    const stream = connectMarketStream(selectedMarket.id, {
      onOrderBook: setOrderBook,
      onTrades: setRecentTrades,
    });

    return () => stream.close();
  }, [selectedMarket, setOrderBook, setRecentTrades]);

  const handleMarketSelect = (market: Market) => {
    setSelectedMarket(market);
    // Update URL without navigation
    window.history.replaceState(null, '', `/exchange?market=${market.id}`);
  };

  const handlePriceClick = (price: number) => {
    setSelectedPrice(price);
  };

  return (
    <>
      {/* Market Header */}
      <div className="border-b px-4 py-2">
        <div className="container flex flex-col gap-3 sm:flex-row sm:items-center sm:gap-4">
          {selectedMarket && (
            <>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-lg font-bold">{selectedMarket.symbol}</span>
                  <Badge variant="outline" className="text-[10px]">SYNTHETIC</Badge>
                </div>
                <div className="text-xs text-muted-foreground">
                  {selectedMarket.base.flagEmoji} {selectedMarket.base.name} / {selectedMarket.quote.flagEmoji} {selectedMarket.quote.name}
                </div>
              </div>
              <div className="grid grid-cols-3 gap-4 text-sm sm:ml-auto sm:flex sm:items-center sm:gap-6">
                <div>
                  <div className="text-muted-foreground text-xs">Last Price</div>
                  <div className="font-mono font-bold">{selectedMarket.lastPrice?.toFixed(4)}</div>
                </div>
                <div>
                  <div className="text-muted-foreground text-xs">24h Change</div>
                  <div className={`font-mono ${(selectedMarket.change24h || 0) >= 0 ? 'text-green-500' : 'text-red-500'}`}>
                    {(selectedMarket.change24h || 0) >= 0 ? '+' : ''}{selectedMarket.change24h?.toFixed(2)}%
                  </div>
                </div>
                <div>
                  <div className="text-muted-foreground text-xs">24h Volume</div>
                  <div className="font-mono">{((selectedMarket.volume24h || 0) / 1000).toFixed(0)}K</div>
                </div>
              </div>
            </>
          )}
        </div>
      </div>

      {/* Main Trading Interface */}
      <div className="flex-1 container py-4">
        <div className="grid grid-cols-1 gap-4 xl:grid-cols-12 xl:h-[calc(100vh-220px)]">
          {/* Market Selector */}
          <Card className="overflow-hidden xl:col-span-2">
            <MarketSelector
              onSelect={handleMarketSelect}
              selectedMarketId={selectedMarket?.id}
            />
          </Card>

          {/* Chart + Order Entry */}
          <div className="flex flex-col gap-4 xl:col-span-7">
            {/* Chart */}
            <Card className="overflow-hidden xl:flex-1">
              <TradingViewChart
                data={chartData}
                height={320}
                onIntervalChange={setChartInterval}
              />
            </Card>

            {/* Orders and Positions */}
            <Card className="overflow-hidden xl:h-48">
              <Tabs defaultValue="orders" className="h-full flex flex-col">
                <TabsList className="w-full justify-start rounded-none border-b">
                  <TabsTrigger value="orders">Open Orders</TabsTrigger>
                  <TabsTrigger value="positions">Positions</TabsTrigger>
                </TabsList>
                <TabsContent value="orders" className="flex-1 m-0 overflow-hidden">
                  <OrderList />
                </TabsContent>
                <TabsContent value="positions" className="flex-1 m-0 overflow-hidden">
                  <PositionList />
                </TabsContent>
              </Tabs>
            </Card>
          </div>

          {/* Order Book + Order Entry */}
          <div className="flex flex-col gap-4 xl:col-span-3">
            {/* Order Book */}
            <Card className="overflow-hidden xl:flex-1">
              <div className="p-2 border-b">
                <span className="text-sm font-medium">Order Book</span>
              </div>
              <div className="h-72 xl:h-[calc(100%-40px)]">
                <OrderBook orderBook={orderBook} onPriceClick={handlePriceClick} />
              </div>
            </Card>

            {/* Order Entry */}
            <Card className="overflow-hidden">
              <OrderEntry market={selectedMarket} selectedPrice={selectedPrice} />
            </Card>

            {/* Recent Trades */}
            <Card className="h-52 overflow-hidden xl:h-40">
              <div className="p-2 border-b">
                <span className="text-sm font-medium">Recent Trades</span>
              </div>
              <div className="h-[calc(100%-40px)]">
                <RecentTrades trades={recentTrades} />
              </div>
            </Card>
          </div>
        </div>
      </div>
    </>
  );
}

export default function ExchangePage() {
  return (
    <div className="min-h-screen flex flex-col bg-background">
      <RiskDisclosure />
      <Navbar />
      <Suspense fallback={
        <div className="flex-1 flex items-center justify-center">
          Loading exchange...
        </div>
      }>
        <ExchangeContent />
      </Suspense>
    </div>
  );
}
