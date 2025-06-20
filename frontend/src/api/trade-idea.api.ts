import type { Watchlist } from '@/interfaces/watchlist.type'
import { apiClient } from './client'

const TRADE_IDEA_API_URL = '/trade-ideas'

export const getTradeIdeas = () => {
  return apiClient.get<Watchlist>(TRADE_IDEA_API_URL)
}
