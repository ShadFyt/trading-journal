import { z } from 'zod'

export const EXECUTION_SIDE = {
  BUY: 'buy',
  SELL: 'sell',
} as const
export const ExecutionSideEnum = z.nativeEnum(EXECUTION_SIDE)

export const EXECUTION_SOURCE = {
  MANUAL: 'manual',
  AUTO: 'auto',
  IMPORT: 'import',
} as const
export const ExecutionSourceEnum = z.nativeEnum(EXECUTION_SOURCE)
