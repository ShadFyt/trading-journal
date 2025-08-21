import { ScalePlanKindEnum } from '@/enums'
import { z } from 'zod'

export const getLimitByKind = (
  positionSize?: number,
): Record<
  (typeof ScalePlanKindEnum.enum)[keyof typeof ScalePlanKindEnum.enum],
  number | undefined
> => ({
  [ScalePlanKindEnum.enum.SHARES]: positionSize,
  [ScalePlanKindEnum.enum.PERCENT]: 100,
})

export const buildTargetPriceIssue = (
  kind: z.infer<typeof ScalePlanKindEnum>,
  positionSize: number,
  newTotal: number,
) => {
  const limitLabel = kind === ScalePlanKindEnum.enum.SHARES ? positionSize : undefined
  return {
    code: z.ZodIssueCode.custom,
    path: ['value'],
    message: `Total planned value (${newTotal.toFixed(2)}) exceeds ${limitLabel}.`,
  }
}

export const addScalePlanLimitIssue = (
  ctx: z.RefinementCtx,
  positionSize: number,
  newTotal: number,
  kind: z.infer<typeof ScalePlanKindEnum>,
) => {
  const limit = getLimitByKind(positionSize)[kind]
  const hasIssue =
    (typeof limit === 'number' && newTotal > limit) ||
    (typeof limit === 'undefined' && newTotal > 100)

  if (hasIssue) {
    const issueObj = buildTargetPriceIssue(kind, positionSize, newTotal)
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
