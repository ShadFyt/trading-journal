import { z } from 'zod'
import { ExecutionSideEnum, ExecutionStatusEnum } from '@/enums'

export const ExecutionSchema = z.object({
  id: z.string().uuid(),
  liveTradeId: z.string().uuid(),
  scale_plan_id: z.string().uuid(),
  price: z.number().min(1, 'Price is required'),
  qty: z.number().min(1, 'Quantity is required'),
  commission: z.number().min(1, 'Cost is required'),
  notes: z.string().optional(),
  executed_at: z.date(),
  side: ExecutionSideEnum,
  source: ExecutionStatusEnum,
})

export const ExecutionCreateSchema = ExecutionSchema.omit({
  id: true,
  executed_at: true,
})

export const ExecutionUpdateSchema = ExecutionCreateSchema.partial()
