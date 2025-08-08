import type { AnnotationSchema, AnnotationCreateSchema } from '@/schemas'
import type z from 'zod'

export type Annotation = z.infer<typeof AnnotationSchema>
export type AnnotationCreate = z.infer<typeof AnnotationCreateSchema>
