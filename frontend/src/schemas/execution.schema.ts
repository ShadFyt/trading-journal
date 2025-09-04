import { z } from 'zod'
import { ExecutionSideEnum, ExecutionSourceEnum } from '@/enums'

export const ExecutionSchema = z.object({
  id: z.string().uuid(),
  tradeId: z.string().uuid(),
  scalePlanId: z.string().uuid(),
  price: z.number().min(1, 'Price is required'),
  qty: z.number().min(1, 'Quantity is required'),
  commission: z.number().min(1, 'Cost is required'),
  notes: z.string().optional(),
  executedAt: z.date(),
  side: ExecutionSideEnum,
  source: ExecutionSourceEnum,
})

export const ExecutionCreateSchema = ExecutionSchema.omit({
  id: true,
  executedAt: true,
})

export const ExecutionUpdateSchema = ExecutionCreateSchema.partial()
