import { ScalePlanCreateSchema, ScalePlanSchema } from '@/schemas'
import { z } from 'zod'

export type ScalePlanCreateType = z.infer<typeof ScalePlanCreateSchema>
export type ScalePlan = z.infer<typeof ScalePlanSchema>
