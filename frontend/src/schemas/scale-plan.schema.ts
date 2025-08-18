import { z } from 'zod'

import { ScalePlanKindEnum, OrderTypeEnum, ScalePlanStatusEnum } from '@/enums/scale-plan.enum'

export const ScalePlanSchema = z.object({
  id: z.string().uuid(),
  liveTradeId: z.string().uuid(),
  kind: ScalePlanKindEnum,
  orderType: OrderTypeEnum,
  label: z.string().min(1, 'Label is required'),
  status: ScalePlanStatusEnum,
  entryPrice: z.number().optional(),
  targetPrice: z.number().optional(),
  value: z.number().min(1, 'Value is required'),
  notes: z.string().optional(),
  goodTillDate: z.date().optional(),
  stopPrice: z.number().optional(),
  limitPrice: z.number().optional(),
})

export const ScalePlanCreateSchema = ScalePlanSchema.omit({
  id: true,
  status: true,
  liveTradeId: true,
})
