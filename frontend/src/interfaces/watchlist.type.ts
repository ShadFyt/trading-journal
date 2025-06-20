export type TradeIdeaStatus = 'waiting' | 'inProgress' | 'invalidated' | 'closed' | 'live'

export interface TradeIdea {
  symbol: string
  status: TradeIdeaStatus
  setupType: string
  rating: number
  entryMax: number
  entryMin: number
  stop: number
  targetPrices: [number, number | undefined]
  rrRatio: number
  catalyst?: string
  ideaDate: string
  notes?: string
}

export type Watchlist = TradeIdea[]
