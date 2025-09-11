import { z } from 'zod'
import { tradeCreateSchema, TradeSchema, LiveTradeUpdateSchema } from '@/schemas/trade.schema.ts'

export type LiveTradeCreate = z.infer<typeof tradeCreateSchema>
export type LiveTrade = z.infer<typeof TradeSchema>
export type LiveTradeUpdate = z.infer<typeof LiveTradeUpdateSchema>
