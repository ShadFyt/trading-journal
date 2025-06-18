export type Status = 'waiting' | 'inProgress' | 'invalidated' | 'closed'

export interface WatchlistItem {
  symbol: string
  status: Status
  setupType: string
  rating: number
  entryRange: string
  stop: number
  target: number
  rr: number
  catalyst?: string
  ideaDate: string
}

export type Watchlist = WatchlistItem[]
