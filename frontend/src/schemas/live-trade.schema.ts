import { z } from 'zod'
import { baseTradeSchema } from './base-trade.schema'
import { AnnotationSchema } from './annotation.schema'
import { ScalePlanCreateSchema, ScalePlanSchema } from './scale-plan.schema'
import { ExecutionSchema } from '@/schemas/execution.schema.ts'

export const liveTradeCreateSchema = baseTradeSchema
  .extend({
    notes: z.string().optional(),
    catalysts: z.string().optional(),
    tradeIdeaId: z.string().uuid(),
    scalePlans: ScalePlanCreateSchema.array(),
  })
  .omit({ targetPrices: true })

export const LiveTradeSchema = liveTradeCreateSchema
  .extend({
    id: z.string().uuid(),
    rrRatio: z.number().optional(),
    outcome: z
      .enum(['big win', 'small win', 'small loss', 'big loss', 'break even', 'pending'])
      .optional(),
    status: z.enum(['open', 'partial', 'closed']),
    exitDate: z.date().optional(),
    enterDate: z.date().optional(),
    annotations: z.array(AnnotationSchema),
    currentPrice: z.number(),
    priceChange: z.number().optional(),
    percentChange: z.number().optional(),
    scalePlans: ScalePlanSchema.array(),
    executions: z.array(ExecutionSchema),
  })
  .omit({ notes: true, catalysts: true })

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
}).partial()
