import type { ScalePlanCreate, ScalePlanUpdate } from '@/interfaces'
import { apiClient } from './client'

const SCALE_PLAN_API_URL = '/scale-plans'

export const createScalePlan = (liveTradeId: string, data: ScalePlanCreate) =>
  apiClient.post(SCALE_PLAN_API_URL, { ...data, liveTradeId })

export const updateScalePlan = (id: string, data: ScalePlanUpdate) =>
  apiClient.patch(`${SCALE_PLAN_API_URL}/${id}`, data)

export const deleteScalePlan = (id: string) => apiClient.delete(`${SCALE_PLAN_API_URL}/${id}`)
