import { render, screen } from '@testing-library/react'
import { MetricCard, MetricBadge } from '@/components/MetricCard'

jest.mock('lucide-react', () => ({
  TrendingUp: () => <span data-testid="trending-up" />,
  TrendingDown: () => <span data-testid="trending-down" />,
  Minus: () => <span data-testid="minus" />,
}))

describe('MetricCard Component', () => {
  it('renders title and value', () => {
    render(<MetricCard title="Test Metric" value="$100" />)
    expect(screen.getByText('Test Metric')).toBeInTheDocument()
    expect(screen.getByText('$100')).toBeInTheDocument()
  })

  it('renders subtitle when provided', () => {
    render(<MetricCard title="Test" value="100" subtitle="test subtitle" />)
    expect(screen.getByText('test subtitle')).toBeInTheDocument()
  })

  it('renders up trend indicator', () => {
    render(<MetricCard title="Test" value="100" trend="up" trendValue="+10%" />)
    expect(screen.getByTestId('trending-up')).toBeInTheDocument()
    expect(screen.getByText('+10%')).toBeInTheDocument()
  })

  it('renders down trend indicator', () => {
    render(<MetricCard title="Test" value="100" trend="down" trendValue="-10%" />)
    expect(screen.getByTestId('trending-down')).toBeInTheDocument()
  })

  it('renders neutral trend indicator', () => {
    render(<MetricCard title="Test" value="100" trend="neutral" trendValue="0%" />)
    expect(screen.getByTestId('minus')).toBeInTheDocument()
  })
})

describe('MetricBadge Component', () => {
  it('renders label and value', () => {
    render(<MetricBadge label="Status" value="Active" />)
    expect(screen.getByText(/Status/)).toBeInTheDocument()
    expect(screen.getByText(/Active/)).toBeInTheDocument()
  })

  it('applies success variant styles', () => {
    const { container } = render(<MetricBadge label="Test" value="1" variant="success" />)
    expect(container.firstChild).toHaveClass('bg-emerald-light')
  })

  it('applies danger variant styles', () => {
    const { container } = render(<MetricBadge label="Test" value="1" variant="danger" />)
    expect(container.firstChild).toHaveClass('bg-rose-light')
  })

  it('applies neutral variant styles by default', () => {
    const { container } = render(<MetricBadge label="Test" value="1" />)
    expect(container.firstChild).toHaveClass('bg-gray-100')
  })
})
