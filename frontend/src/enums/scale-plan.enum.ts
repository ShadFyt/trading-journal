import { z } from 'zod'

export const SCALE_PLAN_KINDS = {
  SHARES: 'shares',
  PERCENT: 'percent',
} as const
export const ScalePlanKindEnum = z.nativeEnum(SCALE_PLAN_KINDS)

export const ORDER_TYPES = {
  MARKET: 'market',
  LIMIT: 'limit',
  STOP: 'stop',
  STOP_LIMIT: 'stop_limit',
} as const
export const OrderTypeEnum = z.nativeEnum(ORDER_TYPES)

export const SCALE_PLAN_STATUSES = {
  PLANNED: 'planned',
  CANCELLED: 'cancelled',
  FILLED: 'filled',
  PARTIALLY_FILLED: 'partially_filled',
  TRIGGERED: 'triggered',
} as const

export const ScalePlanStatusEnum = z.nativeEnum(SCALE_PLAN_STATUSES)
