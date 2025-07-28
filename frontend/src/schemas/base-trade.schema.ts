import { z } from 'zod'

export const baseTradeSchema = z.object({
  symbol: z.string().min(1, 'Symbol is required'),
  setup: z.string().min(1, 'Setup is required'),
  stop: z.number().min(1, 'Stop is required'),
  rating: z.number().min(1, 'Rating is required'),
  targetPrices: z.array(z.number()),
})
