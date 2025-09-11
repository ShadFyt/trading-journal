import { z } from 'zod'

const TRADE_STATUS = {
  OPEN: 'open',
  CLOSED: 'closed',
  WATCHING: 'watching',
  INVALIDATED: 'invalidated',
} as const

export const TradeStatusEnum = z.nativeEnum(TRADE_STATUS)
