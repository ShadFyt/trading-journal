export type TradeStatus = 'open' | 'closed'

export interface Trade {
  symbol: string
  status: TradeStatus
  setupType: string
  rating: number
  entry: number
  stop: number
  shares: number
  targetPrices: number[]
  rr: number
  catalyst?: string
  entryDate: string
  exitDate?: string
  exitReason?: string
  entryReason?: string
  notes?: string
  pnl?: number
  estimatedDuration?: string
}

export type Trades = Trade[]
