import { z } from 'zod'

export const baseTradeSchema = z.object({
  symbol: z
    .string()
    .min(1, 'Symbol is required')
    .transform((val) => val.toUpperCase()),
  setup: z.string().min(1, 'Setup is required'),
  rating: z.number().min(1, 'Rating is required'),
})
