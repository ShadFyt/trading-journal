import { ScalePlanCreateSchema, ScalePlanSchema, ScalePlanUpdateSchema } from '@/schemas'
import { z } from 'zod'

export type ScalePlanCreate = z.infer<typeof ScalePlanCreateSchema>
export type ScalePlan = z.infer<typeof ScalePlanSchema>
export type ScalePlanUpdate = z.infer<typeof ScalePlanUpdateSchema>
