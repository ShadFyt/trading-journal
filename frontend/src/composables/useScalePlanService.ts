import { toast } from 'vue-sonner'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { liveTradeKeys } from '@/composables/useLiveTradeService.ts'
import { createScalePlan, deleteScalePlan, updateScalePlan } from '@/api/scale-plan.api.ts'
import type { ScalePlanCreate, ScalePlanUpdate } from '@/interfaces'
import { handleErrorDisplay } from '@/api/api-error.util.ts'

export const scalePlanKeys = {
  all: ['scalePlan'] as const,
  list: () => [...scalePlanKeys.all, 'list'] as const,
  trade: (id: string) => [...scalePlanKeys.all, 'trade', id] as const,
  detail: (id: string) => [...scalePlanKeys.all, 'detail', id] as const,
}

export const useScalePlanMutationService = () => {
  const queryClient = useQueryClient()

  const domain = 'scale plan'

  const handleSuccess = (type: 'create' | 'update' | 'delete') => {
    queryClient.invalidateQueries({ queryKey: liveTradeKeys.all })
    toast.success(`Scale plan ${type}d successfully`)
  }

  const createMutation = useMutation({
    mutationFn: ({ data, liveTradeId }: { data: ScalePlanCreate; liveTradeId: string }) =>
      createScalePlan(liveTradeId, data),
    onSuccess: () => handleSuccess('create'),
    onError: (e) => handleErrorDisplay(e, 'create', domain),
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: ScalePlanUpdate }) => updateScalePlan(id, data),
    onSuccess: () => handleSuccess('update'),
    onError: (e) => handleErrorDisplay(e, 'update', domain),
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteScalePlan(id),
    onSuccess: () => handleSuccess('delete'),
    onError: (e) => handleErrorDisplay(e, 'delete', domain),
  })

  return {
    deleteMutation,
    createMutation,
    updateMutation,
  }
}

export const useScalePlanValidationService = () => {}
