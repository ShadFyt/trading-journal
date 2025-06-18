export type TradeStatus = 'open' | 'closed'

export interface Trade {
  symbol: string
  status: TradeStatus
  setupType: string
  rating: number
  entry: number
  stop: number
  shares: number
  target: number
  rr: number
  catalyst?: string
  entryDate: string
  exitDate?: string
  exitReason?: string
  entryReason?: string
  notes?: string
  pl?: number
}

export type Trades = Trade[]
