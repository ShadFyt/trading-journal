import type { ScalePlanCreate } from '@/interfaces'

const SCALE_PLAN_API_URL = '/scale-plans'
import { apiClient } from './client'

export const createScalePlan = (liveTradeId: string, data: ScalePlanCreate) =>
  apiClient.post(SCALE_PLAN_API_URL, { ...data, liveTradeId })

export const deleteScalePlan = (id: string) => apiClient.delete(`${SCALE_PLAN_API_URL}/${id}`)
