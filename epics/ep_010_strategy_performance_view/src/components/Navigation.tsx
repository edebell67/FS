'use client'

import { useState } from 'react'
import { Menu, X, TrendingUp, User, LogIn } from 'lucide-react'
import { useStore } from '@/hooks/useStore'
import { cn } from '@/lib/utils'

export function Navigation() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const { user, setShowAuthModal } = useStore()

  return (
    <nav className="sticky top-0 z-50 bg-surface/80 backdrop-blur-xl border-b border-whisper">
      <div className="max-w-7xl mx-auto px-4 md:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 md:h-20">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-ink flex items-center justify-center">
              <TrendingUp className="w-5 h-5 text-white" />
            </div>
            <div>
              <span className="font-semibold text-ink tracking-tight">StrategyView</span>
              <span className="hidden md:inline text-steel text-sm ml-2">Performance Analytics</span>
            </div>
          </div>

          <div className="hidden md:flex items-center gap-8">
            <a href="#dashboard" className="text-sm font-medium text-steel hover:text-ink transition-colors">
              Dashboard
            </a>
            <a href="#strategies" className="text-sm font-medium text-steel hover:text-ink transition-colors">
              Strategies
            </a>
            <a href="#returns" className="text-sm font-medium text-steel hover:text-ink transition-colors">
              Returns
            </a>
          </div>

          <div className="hidden md:flex items-center gap-3">
            {user ? (
              <div className="flex items-center gap-3">
                <span className="text-sm text-steel">{user.name}</span>
                <div className="w-9 h-9 rounded-full bg-emerald-light flex items-center justify-center">
                  <User className="w-4 h-4 text-emerald-signal" />
                </div>
              </div>
            ) : (
              <>
                <button
                  onClick={() => setShowAuthModal('signin')}
                  className="btn-ghost text-sm"
                >
                  Sign In
                </button>
                <button
                  onClick={() => setShowAuthModal('signup')}
                  className="btn-primary text-sm px-5 py-2"
                >
                  Get Started
                </button>
              </>
            )}
          </div>

          <button
            className="md:hidden p-2 -mr-2 text-steel hover:text-ink"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            aria-label="Toggle menu"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      <div
        className={cn(
          'md:hidden absolute top-full left-0 right-0 bg-surface border-b border-whisper',
          'transition-all duration-300 ease-out overflow-hidden',
          mobileMenuOpen ? 'max-h-96 opacity-100' : 'max-h-0 opacity-0'
        )}
      >
        <div className="px-4 py-4 space-y-1">
          <a
            href="#dashboard"
            className="block py-3 px-4 text-sm font-medium text-steel hover:text-ink hover:bg-gray-50 rounded-lg"
            onClick={() => setMobileMenuOpen(false)}
          >
            Dashboard
          </a>
          <a
            href="#strategies"
            className="block py-3 px-4 text-sm font-medium text-steel hover:text-ink hover:bg-gray-50 rounded-lg"
            onClick={() => setMobileMenuOpen(false)}
          >
            Strategies
          </a>
          <a
            href="#returns"
            className="block py-3 px-4 text-sm font-medium text-steel hover:text-ink hover:bg-gray-50 rounded-lg"
            onClick={() => setMobileMenuOpen(false)}
          >
            Returns
          </a>

          <div className="pt-4 border-t border-whisper mt-4 space-y-2">
            {user ? (
              <div className="flex items-center gap-3 px-4 py-2">
                <div className="w-8 h-8 rounded-full bg-emerald-light flex items-center justify-center">
                  <User className="w-4 h-4 text-emerald-signal" />
                </div>
                <span className="text-sm text-steel">{user.name}</span>
              </div>
            ) : (
              <>
                <button
                  onClick={() => {
                    setShowAuthModal('signin')
                    setMobileMenuOpen(false)
                  }}
                  className="w-full flex items-center gap-3 py-3 px-4 text-sm font-medium text-steel hover:text-ink hover:bg-gray-50 rounded-lg"
                >
                  <LogIn className="w-4 h-4" />
                  Sign In
                </button>
                <button
                  onClick={() => {
                    setShowAuthModal('signup')
                    setMobileMenuOpen(false)
                  }}
                  className="w-full btn-primary text-sm"
                >
                  Get Started
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  )
}
