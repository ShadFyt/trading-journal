import { z } from 'zod'
import type { ScalePlanCreate } from '@/interfaces'
import { OrderTypeEnum, ScalePlanTypeEnum, ScaleTradeTypeEnum } from '@/enums'

export const buildTargetPriceIssue = (positionSize: number, newTotal: number) => {
  return {
    code: z.ZodIssueCode.custom,
    path: ['qty'],
    message: `Total planned value (${newTotal.toFixed(2)}) exceeds ${positionSize}.`,
  }
}

export const addScalePlanLimitIssue = (
  ctx: z.RefinementCtx,
  positionSize: number,
  newTotal: number,
) => {
  const hasIssue = newTotal > positionSize
  if (hasIssue) {
    const issueObj = buildTargetPriceIssue(positionSize, newTotal)
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

export const entryPlanFactory = (): ScalePlanCreate => ({
  orderType: OrderTypeEnum.enum.LIMIT,
  label: 'Entry',
  qty: 0,
  targetPrice: 0,
  notes: '',
  stopPrice: 0,
  limitPrice: 0,
  planType: ScalePlanTypeEnum.enum.ENTRY,
  tradeType: ScaleTradeTypeEnum.enum.LONG,
})

export const targetPlanFactory = (idx: number, entryPrice = 0): ScalePlanCreate => ({
  orderType: 'limit',
  label: `Target ${idx}`,
  qty: 0,
  targetPrice: entryPrice + 1,
  notes: '',
  stopPrice: 0,
  limitPrice: 0,
  planType: 'target',
  tradeType: 'long',
})
