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
  PARTIALLY_FILLED: 'filled_partial',
} as const

export const ScalePlanStatusEnum = z.nativeEnum(SCALE_PLAN_STATUSES)

const SCALE_PLAN_TYPES = {
  ENTRY: 'entry',
  TARGET: 'target',
  STOP_LOSS: 'stop_loss',
} as const

export const ScalePlanTypeEnum = z.nativeEnum(SCALE_PLAN_TYPES)
