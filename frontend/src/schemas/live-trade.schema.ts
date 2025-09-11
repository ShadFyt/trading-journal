import { z } from 'zod'
import { baseTradeSchema } from './base-trade.schema'
import { AnnotationSchema } from './annotation.schema'
import { ScalePlanCreateSchema, ScalePlanSchema } from './scale-plan.schema'
import { ExecutionSchema } from '@/schemas/execution.schema.ts'
import { TradeStatusEnum } from '@/enums/trade.enum.ts'
import { ScaleTradeTypeEnum } from '@/enums'

export const tradeCreateSchema = baseTradeSchema.extend({
  scalePlans: ScalePlanCreateSchema.array(),
})

const hasPricesForValidation = (
  plan: any,
): plan is { limitPrice: number; stopPrice: number; tradeType: string } => {
  return typeof plan.limitPrice === 'number' && typeof plan.stopPrice === 'number'
}

export const extendedTradeCreateSchema = tradeCreateSchema.superRefine((data, ctx) => {
  const entryPlans = data.scalePlans.filter((plan) => plan.planType === 'entry')
  if (entryPlans.length === 0) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ['scalePlans'],
      message: 'At least one entry plan is required',
    })
    return
  }

  entryPlans.forEach((plan) => {
    const planIndex = data.scalePlans.findIndex((p) => p === plan)

    if (!hasPricesForValidation(plan)) {
      return
    }

    if (plan.tradeType === ScaleTradeTypeEnum.enum.LONG) {
      if (plan.limitPrice <= plan.stopPrice) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          path: ['scalePlans', planIndex, 'limitPrice'],
          message: 'For long trades, limit price must be greater than stop price',
        })
      }
    } else if (plan.tradeType === ScaleTradeTypeEnum.enum.SHORT) {
      if (plan.limitPrice >= plan.stopPrice) {
        ctx.addIssue({
          code: z.ZodIssueCode.custom,
          path: ['scalePlans', planIndex, 'limitPrice'],
          message: 'For short trades, limit price must be less than stop price',
        })
      }
    }
  })
})

export const LiveTradeSchema = tradeCreateSchema.extend({
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
  status: true,
  scalePlans: true,
  openPrice: true,
  previousClose: true,
}).partial()
