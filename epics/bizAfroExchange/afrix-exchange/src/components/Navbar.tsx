'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { BarChart3, Droplets, Wallet, Settings } from 'lucide-react';

const navItems = [
  { href: '/exchange', label: 'Exchange', icon: BarChart3 },
  { href: '/liquidity', label: 'Liquidity', icon: Droplets },
  { href: '/portfolio', label: 'Portfolio', icon: Wallet },
  { href: '/settings', label: 'Settings', icon: Settings },
];

export function Navbar() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-14 items-center">
        <div className="mr-4 flex">
          <Link href="/" className="mr-6 flex items-center space-x-2">
            <span className="text-xl font-bold bg-gradient-to-r from-green-500 to-emerald-600 bg-clip-text text-transparent">
              AfriX
            </span>
            <Badge variant="outline" className="text-[10px] px-1.5 py-0">
              SYNTHETIC
            </Badge>
          </Link>
        </div>

        <nav className="flex items-center space-x-1 flex-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            return (
              <Link key={item.href} href={item.href}>
                <Button
                  variant={isActive ? 'secondary' : 'ghost'}
                  size="sm"
                  className="gap-2"
                >
                  <Icon className="h-4 w-4" />
                  <span className="hidden sm:inline">{item.label}</span>
                </Button>
              </Link>
            );
          })}
        </nav>

        <div className="flex items-center gap-2">
          <Badge variant="secondary" className="hidden sm:flex">
            Testnet
          </Badge>
          <Button size="sm" variant="outline">
            Connect
          </Button>
        </div>
      </div>
    </header>
  );
}
