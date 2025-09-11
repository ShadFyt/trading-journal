import { z } from 'zod'
import { baseTradeSchema } from './base-trade.schema'
import { AnnotationSchema } from './annotation.schema'
import { ScalePlanCreateSchema, ScalePlanSchema } from './scale-plan.schema'
import { ExecutionSchema } from '@/schemas/execution.schema.ts'
import { TradeStatusEnum } from '@/enums/trade.enum.ts'
import { ScalePlanTypeEnum } from '@/enums'
import {
  addScalePlanLimitIssue,
  validateEntryPlanCount,
  validateEntryPlanPrices,
  validateTargetPlan,
} from '@/utils'

export const tradeCreateSchema = baseTradeSchema.extend({
  scalePlans: ScalePlanCreateSchema.array(),
})

export const extendedTradeCreateSchema = tradeCreateSchema.superRefine((data, ctx) => {
  const entryPlans = data.scalePlans.filter(
    (plan) => plan.planType === ScalePlanTypeEnum.enum.ENTRY,
  )

  if (!validateEntryPlanCount(entryPlans, ctx)) return

  const entryPlan = entryPlans[0]
  const entryPlanIndex = data.scalePlans.findIndex((p) => p === entryPlan)

  validateEntryPlanPrices(entryPlan, entryPlanIndex, ctx)

  const targetPlans = data.scalePlans.filter(
    (plan) => plan.planType === ScalePlanTypeEnum.enum.TARGET,
  )
  const existingTotal = targetPlans.reduce((sum, p) => sum + (p.qty ?? 0), 0)

  targetPlans.forEach((targetPlan) => {
    const planIndex = data.scalePlans.findIndex((p) => p === targetPlan)

    addScalePlanLimitIssue(ctx, entryPlan.qty ?? 0, existingTotal, `scalePlans.${planIndex}.qty`)
    validateTargetPlan(targetPlan, entryPlan, planIndex, ctx)
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
