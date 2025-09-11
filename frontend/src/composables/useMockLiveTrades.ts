import { ref } from 'vue'
import type { LiveTrade } from '@/interfaces/trade.type.ts'
/**
 * Mock data for live trades - realistic swing trading scenarios
 */
export function useMockLiveTrades() {
  const mockTrades = ref<LiveTrade[]>([
    {
      id: 'trade-001-aapl',
      symbol: 'AAPL',
      rating: 5,
      tradeIdeaId: 'idea-001',
      status: 'open',
      entryPriceAvg: 185.5,
      currentPrice: 192.25,
      positionSize: 100,
      stop: 178.0,
      targetPrices: [195.0, 205.0, 215.0],
      entryDate: new Date('2025-07-25'),
      rrRatio: 2.5,
      setup:
        'Bullish breakout above resistance at $185. Strong earnings beat + raised guidance. Tech sector momentum.',
      catalysts: [
        {
          id: 'cat-1',
          date: new Date('2025-07-25'),
          content: 'Earnings beat expectations by 15%, raised full-year guidance',
        },
      ],
      notes: [
        {
          id: 'note-1',
          date: new Date('2025-07-26'),
          content: 'Moved stop to $182 after hitting first resistance level',
        },
      ],
    },
    {
      id: 'trade-002-tsla',
      symbol: 'TSLA',
      rating: 4,
      tradeIdeaId: 'idea-002',
      status: 'partial',
      entryPriceAvg: 245.8,
      currentPrice: 268.5,
      positionSize: 50, // Originally 100, sold 50%
      stop: 235.0,
      targetPrices: [265.0, 285.0, 310.0],
      entryDate: new Date('2025-07-20'),
      rrRatio: 3.0,
      setup: 'Oversold bounce from $240 support. Cybertruck delivery catalyst expected.',
      catalysts: [
        {
          id: 'cat-2',
          date: new Date('2025-07-20'),
          content: 'Cybertruck delivery numbers expected next week',
        },
      ],
      notes: [
        {
          id: 'note-2',
          date: new Date('2025-07-22'),
          content: 'Sold 50% at first target ($265)',
        },
        {
          id: 'note-3',
          date: new Date('2025-07-23'),
          content: 'Trailing stop moved to $255',
        },
      ],
    },
    {
      id: 'trade-003-nvda',
      symbol: 'NVDA',
      rating: 3,
      tradeIdeaId: 'idea-003',
      status: 'open',
      entryPriceAvg: 875.25,
      currentPrice: 862.1,
      positionSize: 25,
      stop: 845.0,
      targetPrices: [920.0, 975.0, 1050.0],
      entryDate: new Date('2025-07-28'),
      rrRatio: 2.8,
      setup:
        'AI chip demand surge. Pullback to 20-day MA provides good entry. Earnings in 2 weeks.',
      catalysts: [
        {
          id: 'cat-3',
          date: new Date('2025-07-28'),
          content: 'AI chip demand surge driving sector rotation',
        },
        {
          id: 'cat-4',
          date: new Date('2025-07-29'),
          content: 'Earnings in 2 weeks - expecting strong data center revenue',
        },
      ],
      notes: [],
    },
    {
      id: 'trade-004-spy',
      rating: 2,
      tradeIdeaId: 'idea-004',
      symbol: 'SPY',
      status: 'open',
      entryPriceAvg: 485.75,
      currentPrice: 491.2,
      positionSize: 200,
      stop: 478.0,
      targetPrices: [495.0, 505.0],
      entryDate: new Date('2025-07-22'),
      rrRatio: 1.8,
      setup:
        'Market bounce from key support. Fed dovish pivot expected. Risk-on sentiment returning.',
      catalysts: [
        {
          id: 'cat-5',
          date: new Date('2025-07-22'),
          content: 'Fed dovish pivot expected - risk-on sentiment returning',
        },
      ],
      notes: [
        {
          id: 'note-4',
          date: new Date('2025-07-22'),
          content: 'Conservative position sizing due to market uncertainty',
        },
      ],
    },
    {
      id: 'trade-005-amd',
      rating: 1,
      tradeIdeaId: 'idea-005',
      symbol: 'AMD',
      status: 'closed',
      entryPriceAvg: 142.3,
      currentPrice: 156.8,
      positionSize: 75,
      stop: 135.0,
      targetPrices: [155.0, 168.0, 180.0],
      entryDate: new Date('2025-07-15'),
      rrRatio: 2.2,
      setup: 'Semiconductor recovery play. Strong data center demand. Oversold from $160 highs.',
      catalysts: [
        {
          id: 'cat-6',
          date: new Date('2025-07-15'),
          content: 'Semiconductor sector rotation - data center demand surge',
        },
      ],
      notes: [
        {
          id: 'note-5',
          date: new Date('2025-07-18'),
          content: 'Closed at first target after strong move',
        },
        {
          id: 'note-6',
          date: new Date('2025-07-19'),
          content: 'Took profits before earnings to reduce risk',
        },
      ],
    },
    {
      id: 'trade-006-msft',
      rating: 5,
      tradeIdeaId: 'idea-006',
      symbol: 'MSFT',
      status: 'open',
      entryPriceAvg: 425.6,
      currentPrice: 438.9,
      positionSize: 50,
      stop: 415.0,
      targetPrices: [445.0, 465.0, 485.0],
      entryDate: new Date('2025-07-26'),
      rrRatio: 2.6,
      setup:
        'Azure growth acceleration. AI integration driving enterprise adoption. Breakout above $425.',
      catalysts: [
        {
          id: 'cat-7',
          date: new Date('2025-07-26'),
          content: 'Azure growth acceleration - AI integration driving adoption',
        },
      ],
      notes: [],
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
      (trade) => (trade.currentPrice - trade.entryPriceAvg) * trade.positionSize > 0,
    ).length
  }

  /**
   * Calculate total portfolio P&L
   */
  const getTotalPnL = () => {
    return mockTrades.value
      .filter((trade) => trade.status !== 'closed')
      .reduce(
        (total, trade) => total + (trade.currentPrice - trade.entryPriceAvg) * trade.positionSize,
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
