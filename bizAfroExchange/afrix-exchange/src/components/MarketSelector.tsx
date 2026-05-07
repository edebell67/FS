'use client';

import { useState, useMemo } from 'react';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { useExchangeStore } from '@/store/useExchangeStore';
import { MARKETS } from '@/constants/currencies';
import { Star, Search } from 'lucide-react';
import type { Market } from '@/types';

interface Props {
  onSelect: (market: Market) => void;
  selectedMarketId?: string;
}

export function MarketSelector({ onSelect, selectedMarketId }: Props) {
  const [search, setSearch] = useState('');
  const [showFavorites, setShowFavorites] = useState(false);

  const { favorites, toggleFavorite } = useExchangeStore();

  const filteredMarkets = useMemo(() => {
    let markets = MARKETS;

    if (showFavorites) {
      markets = markets.filter((m) => favorites.includes(m.id));
    }

    if (search) {
      const searchLower = search.toLowerCase();
      markets = markets.filter(
        (m) =>
          m.symbol.toLowerCase().includes(searchLower) ||
          m.base.name.toLowerCase().includes(searchLower) ||
          m.quote.name.toLowerCase().includes(searchLower)
      );
    }

    return markets;
  }, [search, showFavorites, favorites]);

  return (
    <div className="h-full flex flex-col">
      {/* Search and Filter */}
      <div className="p-2 space-y-2 border-b">
        <div className="relative">
          <Search className="absolute left-2 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Search markets..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-8 h-8 text-sm"
          />
        </div>
        <div className="flex gap-1">
          <Badge
            variant={showFavorites ? 'default' : 'outline'}
            className="cursor-pointer text-xs"
            onClick={() => setShowFavorites(!showFavorites)}
          >
            <Star className="h-3 w-3 mr-1" />
            Favorites
          </Badge>
        </div>
      </div>

      {/* Header */}
      <div className="flex items-center justify-between px-2 py-1.5 text-xs text-muted-foreground border-b">
        <span className="flex-1">Market</span>
        <span className="w-20 text-right">Price</span>
        <span className="w-16 text-right">24h</span>
      </div>

      {/* Markets List */}
      <div className="flex-1 overflow-auto">
        {filteredMarkets.map((market) => {
          const isFavorite = favorites.includes(market.id);
          const isSelected = market.id === selectedMarketId;
          const change = market.change24h || 0;

          return (
            <div
              key={market.id}
              className={`flex items-center justify-between px-2 py-2 cursor-pointer hover:bg-muted/50 transition-colors ${
                isSelected ? 'bg-muted' : ''
              }`}
              onClick={() => onSelect(market)}
            >
              <div className="flex items-center gap-2 flex-1 min-w-0">
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    toggleFavorite(market.id);
                  }}
                  className="flex-shrink-0"
                >
                  <Star
                    className={`h-3.5 w-3.5 ${
                      isFavorite
                        ? 'fill-yellow-500 text-yellow-500'
                        : 'text-muted-foreground hover:text-yellow-500'
                    }`}
                  />
                </button>
                <div className="min-w-0">
                  <div className="text-sm font-medium truncate">
                    {market.symbol}
                  </div>
                  <div className="text-xs text-muted-foreground truncate">
                    {market.base.flagEmoji} / {market.quote.flagEmoji}
                  </div>
                </div>
              </div>
              <div className="w-20 text-right text-sm font-mono">
                {market.lastPrice?.toFixed(4)}
              </div>
              <div
                className={`w-16 text-right text-xs font-medium ${
                  change >= 0 ? 'text-green-500' : 'text-red-500'
                }`}
              >
                {change >= 0 ? '+' : ''}
                {change.toFixed(2)}%
              </div>
            </div>
          );
        })}

        {filteredMarkets.length === 0 && (
          <div className="p-4 text-center text-sm text-muted-foreground">
            No markets found
          </div>
        )}
      </div>
    </div>
  );
}
