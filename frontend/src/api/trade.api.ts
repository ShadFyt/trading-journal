import { apiClient } from './client'
import type { Trade, TradeCreate, TradeUpdate } from '@/interfaces/trade.type.ts'

const LIVE_TRADE_API_URL = '/trades'

export const getLiveTrades = () => {
  return apiClient.get<Trade[]>(LIVE_TRADE_API_URL)
}

export const createLiveTrade = (data: TradeCreate) => {
  const { ...rest } = data

  return apiClient.post<Trade>(LIVE_TRADE_API_URL, {
    ...rest,
  })
}

export const updateLiveTrade = (id: string, data: TradeUpdate) => {
  return apiClient.patch<Trade>(`${LIVE_TRADE_API_URL}/${id}`, data)
}

export const deleteLiveTrade = (id: string) => {
  return apiClient.delete(`${LIVE_TRADE_API_URL}/${id}`)
}

export const replaceTrade = (id: string, data: TradeCreate) => {
  return apiClient.put<Trade>(`${LIVE_TRADE_API_URL}/${id}`, data)
}
