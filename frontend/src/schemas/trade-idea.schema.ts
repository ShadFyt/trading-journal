import { z } from 'zod'

// Define the TradeIdeaStatus enum in TypeScript
export enum TradeIdeaStatus {
  WATCHING = 'Watching',
  IN_PROGRESS = 'InProgress',
  INVALIDATED = 'Invalidated',
  LIVE = 'Live',
  // Add other statuses as needed
}

export const tradeIdeaCreateSchema = z.object({
  symbol: z.string().min(1, 'Symbol is required'),
  setup: z.string().min(1, 'Setup is required'),
  rating: z.number().min(1, 'Rating is required'),
  entryMin: z.number().min(5, 'Entry min is required'),
  entryMax: z.number().optional(),
  stop: z.number().min(1, 'Stop is required'),
  targetPrices: z.array(z.number()),
  catalysts: z.string().optional(),
  notes: z.string().optional(),
})

export const tradeIdeaUpdateSchema = tradeIdeaCreateSchema.partial().extend({
  ideaDate: z.date().or(z.string()),
  status: z.nativeEnum(TradeIdeaStatus),
})

export const tradeIdeaSchema = tradeIdeaCreateSchema.extend({
  id: z.string().uuid(),
  status: z.nativeEnum(TradeIdeaStatus),
  ideaDate: z.date(),
  // riskPerShare: z.number(),
  rrRatio: z.number().optional(),
})
