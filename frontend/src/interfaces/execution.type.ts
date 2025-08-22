import { z } from 'zod'
import {
  ExecutionCreateSchema,
  ExecutionSchema,
  ExecutionUpdateSchema,
} from '@/schemas/execution.schema'

export type ExecutionDto = z.infer<typeof ExecutionSchema>
export type ExecutionCreateDto = z.infer<typeof ExecutionCreateSchema>
export type ExecutionUpdateDto = z.infer<typeof ExecutionUpdateSchema>
