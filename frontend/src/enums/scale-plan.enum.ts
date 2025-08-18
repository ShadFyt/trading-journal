import { z } from 'zod'

export const SCALE_PLAN_KINDS = {
  SHARES: 'shares',
  PERCENT: 'percent',
} as const
export const ScalePlanKindEnum = z.nativeEnum(SCALE_PLAN_KINDS)

export const ORDER_TYPES = ['market', 'limit', 'stop', 'stop_limit'] as const
export const OrderTypeEnum = z.enum(ORDER_TYPES)

export const SCALE_PLAN_STATUSES = [
  'planned',
  'cancelled',
  'filled',
  'partially_filled',
  'triggered',
] as const

export const ScalePlanStatusEnum = z.enum(SCALE_PLAN_STATUSES)
