'use client';

import { useEffect, useRef, useState } from 'react';
import { createChart, IChartApi, ISeriesApi, CandlestickData as TVCandlestickData, UTCTimestamp } from 'lightweight-charts';
import { CandlestickData } from '@/types';
import { Button } from '@/components/ui/button';

interface Props {
  data: CandlestickData[];
  height?: number;
  onIntervalChange?: (interval: string) => void;
}

const intervals = ['1m', '5m', '15m', '1h', '4h', '1D'];

export function TradingViewChart({ data, height = 400, onIntervalChange }: Props) {
  const chartContainerRef = useRef<HTMLDivElement>(null);
  const chartRef = useRef<IChartApi | null>(null);
  const seriesRef = useRef<ISeriesApi<'Candlestick'> | null>(null);
  const [selectedInterval, setSelectedInterval] = useState('1h');

  useEffect(() => {
    if (!chartContainerRef.current) return;

    const chart = createChart(chartContainerRef.current, {
      width: chartContainerRef.current.clientWidth,
      height,
      layout: {
        background: { color: 'transparent' },
        textColor: '#9ca3af',
      },
      grid: {
        vertLines: { color: 'rgba(255, 255, 255, 0.05)' },
        horzLines: { color: 'rgba(255, 255, 255, 0.05)' },
      },
      crosshair: {
        mode: 1,
      },
      rightPriceScale: {
        borderColor: 'rgba(255, 255, 255, 0.1)',
      },
      timeScale: {
        borderColor: 'rgba(255, 255, 255, 0.1)',
        timeVisible: true,
        secondsVisible: false,
      },
    });

    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#22c55e',
      downColor: '#ef4444',
      borderDownColor: '#ef4444',
      borderUpColor: '#22c55e',
      wickDownColor: '#ef4444',
      wickUpColor: '#22c55e',
    });

    // Convert data format
    const chartData: TVCandlestickData<UTCTimestamp>[] = data.map(d => ({
      time: d.time as UTCTimestamp,
      open: d.open,
      high: d.high,
      low: d.low,
      close: d.close,
    }));

    candlestickSeries.setData(chartData);
    chart.timeScale().fitContent();

    chartRef.current = chart;
    seriesRef.current = candlestickSeries;

    const handleResize = () => {
      if (chartContainerRef.current) {
        chart.applyOptions({
          width: chartContainerRef.current.clientWidth,
        });
      }
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      chart.remove();
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [height]);

  // Update data when it changes
  useEffect(() => {
    if (seriesRef.current && data.length > 0) {
      const chartData: TVCandlestickData<UTCTimestamp>[] = data.map(d => ({
        time: d.time as UTCTimestamp,
        open: d.open,
        high: d.high,
        low: d.low,
        close: d.close,
      }));
      seriesRef.current.setData(chartData);
      chartRef.current?.timeScale().fitContent();
    }
  }, [data]);

  const handleIntervalChange = (interval: string) => {
    setSelectedInterval(interval);
    onIntervalChange?.(interval);
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-1 p-2 border-b">
        {intervals.map((interval) => (
          <Button
            key={interval}
            variant={selectedInterval === interval ? 'secondary' : 'ghost'}
            size="sm"
            className="h-7 px-2 text-xs"
            onClick={() => handleIntervalChange(interval)}
          >
            {interval}
          </Button>
        ))}
      </div>
      <div ref={chartContainerRef} className="flex-1" />
    </div>
  );
}
