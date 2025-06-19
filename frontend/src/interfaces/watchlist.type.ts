export type TradeIdeaStatus = 'waiting' | 'inProgress' | 'invalidated' | 'closed' | 'live'

export interface TradeIdea {
  symbol: string
  status: TradeIdeaStatus
  setupType: string
  rating: number
  entryRange: [number, number | undefined]
  stop: number
  targetPrices: [number, number | undefined]
  rr: number
  catalyst?: string
  ideaDate: string
  notes?: string
}

export type Watchlist = TradeIdea[]
