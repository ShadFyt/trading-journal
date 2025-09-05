import { z } from 'zod'
import { baseTradeSchema } from './base-trade.schema'
import { AnnotationSchema } from './annotation.schema'
import { ScalePlanCreateSchema, ScalePlanSchema } from './scale-plan.schema'
import { ExecutionSchema } from '@/schemas/execution.schema.ts'
import { TradeStatusEnum } from '@/enums/trade.enum.ts'

export const liveTradeCreateSchema = baseTradeSchema.extend({
  tradeIdeaId: z.string().uuid(),
  scalePlans: ScalePlanCreateSchema.array(),
})

export const LiveTradeSchema = liveTradeCreateSchema.extend({
  id: z.string().uuid(),
  rrRatio: z.number().optional(),
  outcome: z
    .enum(['big win', 'small win', 'small loss', 'big loss', 'break even', 'pending'])
    .optional(),
  status: TradeStatusEnum,
  exitDate: z.date().optional(),
  enterDate: z.date().optional(),
  annotations: z.array(AnnotationSchema),
  currentPrice: z.number(),
  priceChange: z.number().optional(),
  percentChange: z.number().optional(),
  openPrice: z.number().optional(),
  previousClose: z.number().optional(),
  scalePlans: ScalePlanSchema.array(),
  executions: z.array(ExecutionSchema),
})

export const LiveTradeUpdateSchema = LiveTradeSchema.omit({
  id: true,
  annotations: true,
  priceChange: true,
  percentChange: true,
  currentPrice: true,
  rrRatio: true,
  tradeIdeaId: true,
  status: true,
  scalePlans: true,
  openPrice: true,
  previousClose: true,
}).partial()
