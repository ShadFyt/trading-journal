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
  stopLoss: number
  targetPrices: number[]
  entryDate: Date
  riskRewardRatio: number
  entryReason: string
  managementNotes?: string
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
      stopLoss: 178.0,
      targetPrices: [195.0, 205.0, 215.0],
      entryDate: new Date('2025-07-25'),
      riskRewardRatio: 2.5,
      entryReason:
        'Bullish breakout above resistance at $185. Strong earnings beat + raised guidance. Tech sector momentum.',
      managementNotes: 'Moved stop to $182 after hitting first resistance level.',
    },
    {
      id: 'trade-002-tsla',
      symbol: 'TSLA',
      status: 'partial',
      entryPrice: 245.8,
      currentPrice: 268.5,
      positionSize: 50, // Originally 100, sold 50%
      stopLoss: 235.0,
      targetPrices: [265.0, 285.0, 310.0],
      entryDate: new Date('2025-07-20'),
      riskRewardRatio: 3.0,
      entryReason: 'Oversold bounce from $240 support. Cybertruck delivery catalyst expected.',
      managementNotes: 'Sold 50% at first target ($265). Trailing stop at $255.',
    },
    {
      id: 'trade-003-nvda',
      symbol: 'NVDA',
      status: 'open',
      entryPrice: 875.25,
      currentPrice: 862.1,
      positionSize: 25,
      stopLoss: 845.0,
      targetPrices: [920.0, 975.0, 1050.0],
      entryDate: new Date('2025-07-28'),
      riskRewardRatio: 2.8,
      entryReason:
        'AI chip demand surge. Pullback to 20-day MA provides good entry. Earnings in 2 weeks.',
    },
    {
      id: 'trade-004-spy',
      symbol: 'SPY',
      status: 'open',
      entryPrice: 485.75,
      currentPrice: 491.2,
      positionSize: 200,
      stopLoss: 478.0,
      targetPrices: [495.0, 505.0],
      entryDate: new Date('2025-07-22'),
      riskRewardRatio: 1.8,
      entryReason:
        'Market bounce from key support. Fed dovish pivot expected. Risk-on sentiment returning.',
      managementNotes: 'Conservative position sizing due to market uncertainty.',
    },
    {
      id: 'trade-005-amd',
      symbol: 'AMD',
      status: 'closed',
      entryPrice: 142.3,
      currentPrice: 156.8,
      positionSize: 75,
      stopLoss: 135.0,
      targetPrices: [155.0, 168.0, 180.0],
      entryDate: new Date('2025-07-15'),
      riskRewardRatio: 2.2,
      entryReason:
        'Semiconductor recovery play. Strong data center demand. Oversold from $160 highs.',
      managementNotes: 'Closed at first target after strong move. Took profits before earnings.',
    },
    {
      id: 'trade-006-msft',
      symbol: 'MSFT',
      status: 'open',
      entryPrice: 425.6,
      currentPrice: 438.9,
      positionSize: 50,
      stopLoss: 415.0,
      targetPrices: [445.0, 465.0, 485.0],
      entryDate: new Date('2025-07-26'),
      riskRewardRatio: 2.6,
      entryReason:
        'Azure growth acceleration. AI integration driving enterprise adoption. Breakout above $425.',
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
   * Get profitable positions
   */
  const getProfitablePositions = () => {
    return mockTrades.value.filter(
      (trade) => (trade.currentPrice - trade.entryPrice) * trade.positionSize > 0,
    ).length
  }

  /**
   * Calculate total portfolio P&L
   */
  const getTotalPnL = () => {
    return mockTrades.value
      .filter((trade) => trade.status !== 'closed')
      .reduce(
        (total, trade) => total + (trade.currentPrice - trade.entryPrice) * trade.positionSize,
        0,
      )
  }

  /**
   * Calculate total portfolio value
   */
  const getTotalPortfolioValue = () => {
    return mockTrades.value
      .filter((trade) => trade.status !== 'closed')
      .reduce((total, trade) => total + trade.positionSize * trade.currentPrice, 0)
  }

  return {
    mockTrades,
    getTradesByStatus,
    getActiveTrades,
    getProfitablePositions,
    getTotalPnL,
    getTotalPortfolioValue,
  }
}

export type { LiveTrade }
