import { z } from 'zod'
import type { ScalePlanCreate } from '@/interfaces'
import { OrderTypeEnum, ScalePlanTypeEnum, ScaleTradeTypeEnum } from '@/enums'

export const buildTargetPriceIssue = (positionSize: number, newTotal: number, path?: string) => {
  return {
    code: z.ZodIssueCode.custom,
    path: [path ?? 'qty'],
    message: `Total planned value (${newTotal.toFixed(2)}) exceeds ${positionSize}.`,
  }
}

export const addScalePlanLimitIssue = (
  ctx: z.RefinementCtx,
  positionSize: number,
  newTotal: number,
  path?: string,
) => {
  const hasIssue = newTotal > positionSize
  if (hasIssue) {
    const issueObj = buildTargetPriceIssue(positionSize, newTotal, path)
    ctx.addIssue(issueObj)
  }
}

export const addScalePlanTargetPriceIssue = (
  ctx: z.RefinementCtx,
  nextTarget: number | undefined,
  entryPrice: number | undefined,
) => {
  // TODO: account for short positions
  const hasNumbers = typeof nextTarget === 'number' && typeof entryPrice === 'number'
  if (!hasNumbers) return
  if (nextTarget < entryPrice) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ['targetPrice'],
      message: `Target price must be ≥ entry price (${entryPrice.toFixed(2)}).`,
    })
  }
}

const hasPricesForValidation = (
  plan: any,
): plan is { limitPrice: number; stopPrice: number; tradeType: string } => {
  return typeof plan.limitPrice === 'number' && typeof plan.stopPrice === 'number'
}

export const validateEntryPlanCount = (entryPlans: any[], ctx: z.RefinementCtx): boolean => {
  if (entryPlans.length !== 1) {
    const message =
      entryPlans.length === 0 ? 'One entry plan is required' : 'Only one entry plan is allowed'
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ['scalePlans'],
      message,
    })
    return false
  }
  return true
}

export const validateEntryPlanPrices = (
  entryPlan: ScalePlanCreate,
  planIndex: number,
  ctx: z.RefinementCtx,
): void => {
  if (!hasPricesForValidation(entryPlan)) return

  const isLong = entryPlan.tradeType === ScaleTradeTypeEnum.enum.LONG
  const isShort = entryPlan.tradeType === ScaleTradeTypeEnum.enum.SHORT

  if (isLong && entryPlan.limitPrice <= entryPlan.stopPrice) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ['scalePlans', planIndex, 'limitPrice'],
      message: 'For long trades, limit price must be greater than stop price',
    })
  } else if (isShort && entryPlan.limitPrice >= entryPlan.stopPrice) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ['scalePlans', planIndex, 'limitPrice'],
      message: 'For short trades, limit price must be less than stop price',
    })
  }
}

export const validateTargetPlan = (
  targetPlan: ScalePlanCreate,
  entryPlan: ScalePlanCreate,
  planIndex: number,
  ctx: z.RefinementCtx,
): void => {
  const entryPrice = entryPlan.limitPrice ?? 0

  if (!targetPlan.targetPrice) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ['scalePlans', planIndex, 'targetPrice'],
      message: 'Target price is required',
    })
    return
  }

  const isLong = entryPlan.tradeType === ScaleTradeTypeEnum.enum.LONG
  const isShort = entryPlan.tradeType === ScaleTradeTypeEnum.enum.SHORT

  if (isLong && targetPlan.targetPrice <= entryPrice) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ['scalePlans', planIndex, 'targetPrice'],
      message: 'For long trades, target price must be greater than limit price',
    })
  } else if (isShort && targetPlan.targetPrice >= entryPrice) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ['scalePlans', planIndex, 'targetPrice'],
      message: 'For short trades, target price must be less than limit price',
    })
  }
}

export const entryPlanFactory = (): ScalePlanCreate => ({
  orderType: OrderTypeEnum.enum.LIMIT,
  label: 'Entry',
  qty: 1,
  targetPrice: 0,
  notes: '',
  stopPrice: 0,
  limitPrice: 1,
  planType: ScalePlanTypeEnum.enum.ENTRY,
  tradeType: ScaleTradeTypeEnum.enum.LONG,
})

export const targetPlanFactory = (idx: number, entryPrice = 0): ScalePlanCreate => ({
  label: `Target ${idx}`,
  qty: 0,
  targetPrice: entryPrice + 1,
  notes: '',
  stopPrice: 0,
  limitPrice: 0,
  planType: 'target',
  tradeType: 'long',
  orderType: OrderTypeEnum.enum.LIMIT,
})
