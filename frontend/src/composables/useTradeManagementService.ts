import { toast } from 'vue-sonner'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { liveTradeKeys } from '@/composables/useLiveTradeService.ts'
import { createScalePlan, deleteScalePlan, updateScalePlan } from '@/api/scale-plan.api.ts'
import type { ExecutionCreateDto, ScalePlanCreate, ScalePlanUpdate } from '@/interfaces'
import { handleErrorDisplay } from '@/api/api-error.util.ts'
import { executePlan } from '@/api'

export const scalePlanKeys = {
  all: ['scalePlan'] as const,
  list: () => [...scalePlanKeys.all, 'list'] as const,
  trade: (id: string) => [...scalePlanKeys.all, 'trade', id] as const,
  detail: (id: string) => [...scalePlanKeys.all, 'detail', id] as const,
}

export const useScalePlanMutations = () => {
  const queryClient = useQueryClient()

  const domain = 'scale plan'

  const handleSuccess = (type: 'create' | 'update' | 'delete') => {
    queryClient.invalidateQueries({ queryKey: liveTradeKeys.all })
    toast.success(`Scale plan ${type}d successfully`)
  }

  const createPlanMutation = useMutation({
    mutationFn: ({ data, liveTradeId }: { data: ScalePlanCreate; liveTradeId: string }) =>
      createScalePlan(liveTradeId, data),
    onSuccess: () => handleSuccess('create'),
    onError: (e) => handleErrorDisplay(e, 'create', domain),
  })

  const updatePlanMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: ScalePlanUpdate }) => updateScalePlan(id, data),
    onSuccess: () => handleSuccess('update'),
    onError: (e) => handleErrorDisplay(e, 'update', domain),
  })

  const deletePlanMutation = useMutation({
    mutationFn: (id: string) => deleteScalePlan(id),
    onSuccess: () => handleSuccess('delete'),
    onError: (e) => handleErrorDisplay(e, 'delete', domain),
  })

  return {
    deletePlanMutation,
    createPlanMutation,
    updatePlanMutation,
  }
}

export const useTradeExecutionMutations = () => {
  const queryClient = useQueryClient()
  const domain = 'trade execution'

  const handleSuccess = () => {
    queryClient.invalidateQueries({ queryKey: liveTradeKeys.all })
    toast.success(`Executed plan successfully`)
  }

  const executePlanMutation = useMutation({
    mutationFn: (payload: ExecutionCreateDto) => executePlan(payload),
    onSuccess: () => handleSuccess(),
    onError: (e) => handleErrorDisplay(e, 'create', domain),
  })

  return {
    executePlanMutation,
  }
}
