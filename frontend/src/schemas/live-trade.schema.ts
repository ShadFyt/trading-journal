import { z } from 'zod'
import { baseTradeSchema } from './base-trade.schema'

const AnnotationSchema = z.object({
  id: z.string().uuid(),
  content: z.string(),
  date: z.date(),
  type: z.enum(['note', 'catalyst']),
})

export const liveTradeCreateSchema = baseTradeSchema.extend({
  entryPriceAvg: z.number().min(1, 'Entry price is required'),
  exitPriceAvg: z.number().optional(),
  positionSize: z.number().min(1, 'Position size is required'),
  notes: z.array(z.string()).optional(),
  catalysts: z.array(z.string()).optional(),
  tradeIdeaId: z.string().uuid(),
})

export const LiveTradeSchema = liveTradeCreateSchema.extend({
  id: z.string().uuid(),
  rrRatio: z.number().optional(),
  outcome: z.string().optional(),
  status: z.enum(['open', 'partial', 'closed']),
  exitDate: z.date().optional(),
  enterDate: z.date(),
  commissions: z.number().optional(),
  annotations: z.array(AnnotationSchema),
  currentPrice: z.number(),
  priceChange: z.number().optional(),
  percentChange: z.number().optional(),
})

export const LiveTradeUpdateSchema = LiveTradeSchema.omit({ id: true })
