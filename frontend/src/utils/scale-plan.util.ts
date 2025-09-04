import { z } from 'zod'

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
