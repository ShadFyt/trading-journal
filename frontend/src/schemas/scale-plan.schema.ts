import { z } from 'zod'

import {
  OrderTypeEnum,
  ScalePlanStatusEnum,
  ScalePlanTypeEnum,
  ScaleTradeTypeEnum,
} from '@/enums/scale-plan.enum'
import { ExecutionSchema } from '@/schemas/execution.schema.ts'

export const ScalePlanSchema = z.object({
  id: z.string().uuid(),
  tradeId: z.string().uuid(),
  orderType: OrderTypeEnum,
  label: z.string().min(1, 'Label is required'),
  status: ScalePlanStatusEnum,
  planType: ScalePlanTypeEnum,
  targetPrice: z.number().optional(),
  qty: z.number().min(1, 'Qty is required'),
  notes: z.string().optional(),
  goodTillDate: z.date().optional(),
  stopPrice: z.number().optional(),
  limitPrice: z.number().optional(),
  executions: z.array(ExecutionSchema),
  tradeType: ScaleTradeTypeEnum,
})

export const ScalePlanCreateSchema = ScalePlanSchema.omit({
  id: true,
  status: true,
  tradeId: true,
  executions: true,
})

export const ScalePlanUpdateSchema = ScalePlanSchema.omit({
  id: true,
  tradeId: true,
  executions: true,
}).partial()
