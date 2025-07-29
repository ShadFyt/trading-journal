import { ref } from 'vue'

/**
 * Live trade data interface
 */
interface LiveTrade {
  id: string
  symbol: string
  status: 'open' | 'partial' | 'closed'
  entryPrice: number
  currentPrice: number
  positionSize: number
  positionValue: number
  stopLoss: number
  targetPrices: number[]
  entryDate: Date
  pnl: number
  pnlPercentage: number
  riskRewardRatio: number
  entryReason: string
  managementNotes?: string
  timeInTrade: string
}

/**
 * Mock data for live trades - realistic swing trading scenarios
 */
export function useMockLiveTrades() {
  const mockTrades = ref<LiveTrade[]>([
    {
      id: 'trade-001-aapl',
      symbol: 'AAPL',
      status: 'open',
      entryPrice: 185.5,
      currentPrice: 192.25,
      positionSize: 100,
      positionValue: 19225,
      stopLoss: 178.0,
      targetPrices: [195.0, 205.0, 215.0],
      entryDate: new Date('2025-01-25'),
      pnl: 675.0,
      pnlPercentage: 3.64,
      riskRewardRatio: 2.5,
      entryReason:
        'Bullish breakout above resistance at $185. Strong earnings beat + raised guidance. Tech sector momentum.',
      managementNotes: 'Moved stop to $182 after hitting first resistance level.',
      timeInTrade: '4 days',
    },
    {
      id: 'trade-002-tsla',
      symbol: 'TSLA',
      status: 'partial',
      entryPrice: 245.8,
      currentPrice: 268.5,
      positionSize: 50, // Originally 100, sold 50%
      positionValue: 13425,
      stopLoss: 235.0,
      targetPrices: [265.0, 285.0, 310.0],
      entryDate: new Date('2025-01-20'),
      pnl: 1135.0,
      pnlPercentage: 9.23,
      riskRewardRatio: 3.0,
      entryReason: 'Oversold bounce from $240 support. Cybertruck delivery catalyst expected.',
      managementNotes: 'Sold 50% at first target ($265). Trailing stop at $255.',
      timeInTrade: '9 days',
    },
    {
      id: 'trade-003-nvda',
      symbol: 'NVDA',
      status: 'open',
      entryPrice: 875.25,
      currentPrice: 862.1,
      positionSize: 25,
      positionValue: 21552.5,
      stopLoss: 845.0,
      targetPrices: [920.0, 975.0, 1050.0],
      entryDate: new Date('2025-01-28'),
      pnl: -328.75,
      pnlPercentage: -1.5,
      riskRewardRatio: 2.8,
      entryReason:
        'AI chip demand surge. Pullback to 20-day MA provides good entry. Earnings in 2 weeks.',
      timeInTrade: '1 day',
    },
    {
      id: 'trade-004-spy',
      symbol: 'SPY',
      status: 'open',
      entryPrice: 485.75,
      currentPrice: 491.2,
      positionSize: 200,
      positionValue: 98240,
      stopLoss: 478.0,
      targetPrices: [495.0, 505.0],
      entryDate: new Date('2025-01-22'),
      pnl: 1090.0,
      pnlPercentage: 1.12,
      riskRewardRatio: 1.8,
      entryReason:
        'Market bounce from key support. Fed dovish pivot expected. Risk-on sentiment returning.',
      managementNotes: 'Conservative position sizing due to market uncertainty.',
      timeInTrade: '7 days',
    },
    {
      id: 'trade-005-amd',
      symbol: 'AMD',
      status: 'closed',
      entryPrice: 142.3,
      currentPrice: 156.8,
      positionSize: 75,
      positionValue: 11760,
      stopLoss: 135.0,
      targetPrices: [155.0, 168.0, 180.0],
      entryDate: new Date('2025-01-15'),
      pnl: 1087.5,
      pnlPercentage: 10.2,
      riskRewardRatio: 2.2,
      entryReason:
        'Semiconductor recovery play. Strong data center demand. Oversold from $160 highs.',
      managementNotes: 'Closed at first target after strong move. Took profits before earnings.',
      timeInTrade: '14 days',
    },
    {
      id: 'trade-006-msft',
      symbol: 'MSFT',
      status: 'open',
      entryPrice: 425.6,
      currentPrice: 438.9,
      positionSize: 50,
      positionValue: 21945,
      stopLoss: 415.0,
      targetPrices: [445.0, 465.0, 485.0],
      entryDate: new Date('2025-01-26'),
      pnl: 665.0,
      pnlPercentage: 3.12,
      riskRewardRatio: 2.6,
      entryReason:
        'Azure growth acceleration. AI integration driving enterprise adoption. Breakout above $425.',
      timeInTrade: '3 days',
    },
  ])

  /**
   * Get trades filtered by status
   */
  const getTradesByStatus = (status?: 'open' | 'partial' | 'closed') => {
    if (!status) return mockTrades.value
    return mockTrades.value.filter((trade) => trade.status === status)
  }

  /**
   * Get active trades (open + partial)
   */
  const getActiveTrades = () => {
    return mockTrades.value.filter((trade) => trade.status !== 'closed')
  }

  /**
   * Calculate total portfolio P&L
   */
  const getTotalPnL = () => {
    return mockTrades.value
      .filter((trade) => trade.status !== 'closed')
      .reduce((total, trade) => total + trade.pnl, 0)
  }

  /**
   * Calculate total portfolio value
   */
  const getTotalPortfolioValue = () => {
    return mockTrades.value
      .filter((trade) => trade.status !== 'closed')
      .reduce((total, trade) => total + trade.positionValue, 0)
  }

  return {
    mockTrades,
    getTradesByStatus,
    getActiveTrades,
    getTotalPnL,
    getTotalPortfolioValue,
  }
}

export type { LiveTrade }
