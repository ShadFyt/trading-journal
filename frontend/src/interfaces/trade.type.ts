import { z } from 'zod'
import { tradeCreateSchema, TradeSchema, LiveTradeUpdateSchema } from '@/schemas/trade.schema.ts'

export type TradeCreate = z.infer<typeof tradeCreateSchema>
export type Trade = z.infer<typeof TradeSchema>
export type TradeUpdate = z.infer<typeof LiveTradeUpdateSchema>
