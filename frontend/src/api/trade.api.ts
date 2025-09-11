import { apiClient } from './client'
import type { LiveTrade, LiveTradeCreate, LiveTradeUpdate } from '@/interfaces/trade.type.ts'

const LIVE_TRADE_API_URL = '/trades'

export const getLiveTrades = () => {
  return apiClient.get<LiveTrade[]>(LIVE_TRADE_API_URL)
}

export const createLiveTrade = (data: LiveTradeCreate) => {
  const { ...rest } = data

  return apiClient.post<LiveTrade>(LIVE_TRADE_API_URL, {
    ...rest,
  })
}

export const updateLiveTrade = (id: string, data: LiveTradeUpdate) => {
  return apiClient.patch<LiveTrade>(`${LIVE_TRADE_API_URL}/${id}`, data)
}

export const deleteLiveTrade = (id: string) => {
  return apiClient.delete(`${LIVE_TRADE_API_URL}/${id}`)
}
