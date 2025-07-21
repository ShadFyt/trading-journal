import { tradeIdeaCreateSchema } from '@/schemas'
import type z from 'zod'
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
  catalysts?: string
  ideaDate: string
  notes?: string
}

export type Watchlist = TradeIdea[]

export type TradeIdeaCreate = z.infer<typeof tradeIdeaCreateSchema>
