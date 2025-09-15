import { apiClient } from './client'
import type { Trade, TradeCreate, TradeUpdate } from '@/interfaces/trade.type.ts'

const TRADE_API_URL = '/trades'

export const getTrades = () => {
  return apiClient.get<Trade[]>(TRADE_API_URL)
}

export const createTrade = (data: TradeCreate) => {
  const { ...rest } = data

  return apiClient.post<Trade>(TRADE_API_URL, {
    ...rest,
  })
}

export const updateTrade = (id: string, data: TradeUpdate) => {
  return apiClient.patch<Trade>(`${TRADE_API_URL}/${id}`, data)
}

export const deleteTrade = (id: string) => {
  return apiClient.delete(`${TRADE_API_URL}/${id}`)
}

export const replaceTrade = (id: string, data: TradeCreate) => {
  return apiClient.put<Trade>(`${TRADE_API_URL}/${id}`, data)
}

export const invalidateTrade = (id: string) => {
  return apiClient.patch(`${TRADE_API_URL}/${id}/invalidate`)
}
