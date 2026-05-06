import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        canvas: '#F9FAFB',
        surface: '#FFFFFF',
        ink: '#18181B',
        steel: '#71717A',
        muted: '#94A3B8',
        whisper: 'rgba(226,232,240,0.5)',
        emerald: {
          signal: '#10B981',
          light: '#D1FAE5',
        },
        rose: {
          deep: '#E11D48',
          light: '#FFE4E6',
        },
        electric: '#3B82F6',
      },
      fontFamily: {
        sans: ['Geist', 'system-ui', 'sans-serif'],
        mono: ['Geist Mono', 'JetBrains Mono', 'monospace'],
      },
      borderRadius: {
        '2xl': '1rem',
        '3xl': '1.5rem',
        '4xl': '2rem',
      },
      boxShadow: {
        diffuse: '0 20px 40px -15px rgba(0,0,0,0.05)',
        card: '0 1px 3px rgba(0,0,0,0.04)',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s cubic-bezier(0.32, 0.72, 0, 1)',
        'slide-up': 'slideUp 0.5s cubic-bezier(0.32, 0.72, 0, 1)',
        'pulse-soft': 'pulseSoft 2s ease-in-out infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { opacity: '0', transform: 'translateY(16px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.7' },
        },
      },
    },
  },
  plugins: [],
}
export default config
