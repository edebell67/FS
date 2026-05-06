import type { OrderBook, Trade } from '@/types';
import { mockAPI } from '@/lib/api/mock';

export interface MarketStreamHandlers {
  onOrderBook: (data: OrderBook) => void;
  onTrades: (data: Trade[]) => void;
  onError?: (error: unknown) => void;
}

export interface MarketStream {
  close: () => void;
}

export function connectMarketStream(
  marketId: string,
  handlers: MarketStreamHandlers
): MarketStream {
  let closed = false;

  const tick = async () => {
    if (closed) return;
    try {
      const [orderBook, trades] = await Promise.all([
        mockAPI.getOrderBook(marketId),
        mockAPI.getTrades(marketId),
      ]);
      if (!closed) {
        handlers.onOrderBook(orderBook);
        handlers.onTrades(trades);
      }
    } catch (error) {
      handlers.onError?.(error);
    }
  };

  void tick();
  const intervalId = window.setInterval(() => {
    void tick();
  }, 2000);

  return {
    close: () => {
      closed = true;
      window.clearInterval(intervalId);
    },
  };
}
