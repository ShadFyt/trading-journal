const SCALE_PLAN_API_URL = '/scale-plans'
import { apiClient } from './client'

export const deleteScalePlan = (id: string) => apiClient.delete(`${SCALE_PLAN_API_URL}/${id}`)
