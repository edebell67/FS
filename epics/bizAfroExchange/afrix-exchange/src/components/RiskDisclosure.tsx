'use client';

import { AlertTriangle } from 'lucide-react';

interface RiskDisclosureProps {
  variant?: 'banner' | 'inline';
}

export function RiskDisclosure({ variant = 'banner' }: RiskDisclosureProps) {
  if (variant === 'inline') {
    return (
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <AlertTriangle className="h-4 w-4 text-yellow-500" />
        <span>Synthetic instruments only. Not real currency settlement.</span>
      </div>
    );
  }

  return (
    <div className="bg-yellow-500/10 border border-yellow-500/20 px-4 py-2">
      <div className="container flex items-center justify-center gap-2 text-sm">
        <AlertTriangle className="h-4 w-4 text-yellow-500 flex-shrink-0" />
        <span className="text-yellow-600 dark:text-yellow-400">
          <strong>Risk Warning:</strong> AfriX trades synthetic instruments only.
          No real African currency settlement or banking integration.
          Settlement is in SETTLE tokens only.
        </span>
      </div>
    </div>
  );
}
