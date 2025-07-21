import type { TradeIdeaCreate, Watchlist } from '@/interfaces/trade-idea.type'
import { apiClient } from './client'

const TRADE_IDEA_API_URL = '/trade-ideas'

export const getTradeIdeas = () => {
  return apiClient.get<Watchlist>(TRADE_IDEA_API_URL)
}
