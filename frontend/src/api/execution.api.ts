import { apiClient } from './client'
import type { ExecutionCreateDto, ExecutionDto, ExecutionUpdateDto } from '@/interfaces'
const EXECUTION_API_URL = '/executions'

export const fetchExecutions = (tradeId?: string) =>
  apiClient.get<ExecutionDto[]>(EXECUTION_API_URL, {
    params: {
      tradeId,
    },
  })

export const executePlan = (payload: ExecutionCreateDto) =>
  apiClient.post(`${EXECUTION_API_URL}/execute`, payload)

export const updateExecution = (id: string, payload: ExecutionUpdateDto) => {
  return apiClient.patch(`${EXECUTION_API_URL}/${id}`, payload)
}

export const deleteExecution = (id: string) => {
  return apiClient.delete(`${EXECUTION_API_URL}/${id}`)
}
