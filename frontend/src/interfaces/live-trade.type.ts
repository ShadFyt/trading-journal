import { z } from 'zod'
import {
  liveTradeCreateSchema,
  LiveTradeSchema,
  LiveTradeUpdateSchema,
  AnnotationSchema,
} from '@/schemas/live-trade.schema'

export type LiveTradeCreate = z.infer<typeof liveTradeCreateSchema>
export type LiveTrade = z.infer<typeof LiveTradeSchema>
export type LiveTradeUpdate = z.infer<typeof LiveTradeUpdateSchema>
export type Annotation = z.infer<typeof AnnotationSchema>
