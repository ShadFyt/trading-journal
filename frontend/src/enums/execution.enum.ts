import { z } from 'zod'

export const EXECUTION_SIDE = {
  BUY: 'buy',
  SELL: 'sell',
} as const
export const ExecutionSideEnum = z.nativeEnum(EXECUTION_SIDE)

export const EXECUTION_SOURCE = {
  MANUAL: 'MANUAL',
  AUTO: 'AUTOMATED',
  IMPORT: 'IMPORT',
} as const
export const ExecutionSourceEnum = z.nativeEnum(EXECUTION_SOURCE)
