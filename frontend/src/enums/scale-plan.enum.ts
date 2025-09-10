import { z } from 'zod'

export const ORDER_TYPES = {
  MARKET: 'market',
  LIMIT: 'limit',
  STOP: 'stop',
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

const SCALE_TRADE_TYPES = {
  LONG: 'long',
  SHORT: 'short',
} as const

export const ScaleTradeTypeEnum = z.nativeEnum(SCALE_TRADE_TYPES)
