import { z } from 'zod'
import {
  tradeCreateSchema,
  LiveTradeSchema,
  LiveTradeUpdateSchema,
} from '@/schemas/live-trade.schema'

export type LiveTradeCreate = z.infer<typeof tradeCreateSchema>
export type LiveTrade = z.infer<typeof LiveTradeSchema>
export type LiveTradeUpdate = z.infer<typeof LiveTradeUpdateSchema>
