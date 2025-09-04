import { z } from 'zod'

export const AnnotationSchema = z.object({
  id: z.string().uuid(),
  content: z.string(),
  date: z.date(),
  type: z.enum(['note', 'catalyst']),
  tradeId: z.string().uuid(),
})

export const AnnotationCreateSchema = AnnotationSchema.omit({ id: true, date: true })
