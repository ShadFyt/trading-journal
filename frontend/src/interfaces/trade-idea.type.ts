import { tradeIdeaCreateSchema, tradeIdeaSchema } from '@/schemas'
import type z from 'zod'
export type TradeIdeaStatus = 'waiting' | 'inProgress' | 'invalidated' | 'closed' | 'live'

export type TradeIdea = z.infer<typeof tradeIdeaSchema>

export type Watchlist = TradeIdea[]

export type TradeIdeaCreate = z.infer<typeof tradeIdeaCreateSchema>
