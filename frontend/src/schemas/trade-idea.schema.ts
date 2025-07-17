import { z } from 'zod'

// Define the TradeIdeaStatus enum in TypeScript
export enum TradeIdeaStatus {
  WATCHING = 'WATCHING',
  IN_PROGRESS = 'IN_PROGRESS',
  INVALIDATED = 'INVALIDATED',
  LIVE = 'LIVE',
  // Add other statuses as needed
}

export const tradeIdeaCreateSchema = z.object({
  symbol: z.string().min(1, 'Symbol is required'),
  setup: z.string().min(1, 'Setup is required'),
  rating: z.number().int().min(1, 'Rating is required'),
  entryMin: z.number().min(5, 'Entry min is required'),
  entryMax: z.number().optional(),
  stop: z.number().optional(),
  targetPrices: z.array(z.number()),
  catalysts: z.string().optional(),
  ideaDate: z.date().default(() => new Date()),
  notes: z.string().optional(),
  rrRatio: z.number().optional(),
})
