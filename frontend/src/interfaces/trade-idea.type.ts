import { tradeIdeaCreateSchema, tradeIdeaSchema, tradeIdeaUpdateSchema } from '@/schemas'
import type z from 'zod'
export type TradeIdeaStatus = 'Watching' | 'InProgress' | 'Invalidated' | 'Closed' | 'Live'

export type TradeIdea = z.infer<typeof tradeIdeaSchema>

export type Watchlist = TradeIdea[]

export type TradeIdeaCreate = z.infer<typeof tradeIdeaCreateSchema>

export type TradeIdeaUpdate = z.infer<typeof tradeIdeaUpdateSchema>

export type TradeIdeaFormValues = TradeIdeaCreate | TradeIdeaUpdate
