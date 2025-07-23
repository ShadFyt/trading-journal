import type { TradeIdeaCreate, TradeIdeaUpdate, Watchlist } from '@/interfaces/trade-idea.type'
import { apiClient } from './client'

const TRADE_IDEA_API_URL = '/trade-ideas'

export const getTradeIdeas = () => {
  return apiClient.get<Watchlist>(TRADE_IDEA_API_URL)
}

export const createTradeIdea = (data: TradeIdeaCreate) => {
  return apiClient.post<TradeIdeaCreate>(TRADE_IDEA_API_URL, data)
}

export const updateTradeIdea = (id: string, data: TradeIdeaUpdate) => {
  return apiClient.patch(`${TRADE_IDEA_API_URL}/${id}`, data)
}

export const deleteTradeIdea = (id: string) => {
  return apiClient.delete(`${TRADE_IDEA_API_URL}/${id}`)
}
