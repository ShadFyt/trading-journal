import { toast } from 'vue-sonner'
import { AxiosError } from 'axios'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { liveTradeKeys } from '@/composables/useLiveTradeService.ts'
import { createScalePlan, deleteScalePlan, updateScalePlan } from '@/api/scale-plan.api.ts'
import type { ScalePlanCreate, ScalePlanUpdate } from '@/interfaces'
import { NormalizedErrorSchema } from '@/api/api-error.util.ts'

export const scalePlanKeys = {
  all: ['scalePlan'] as const,
  list: () => [...scalePlanKeys.all, 'list'] as const,
  trade: (id: string) => [...scalePlanKeys.all, 'trade', id] as const,
  detail: (id: string) => [...scalePlanKeys.all, 'detail', id] as const,
}

export const useScalePlanMutationService = () => {
  const queryClient = useQueryClient()

  const handleError = (e: unknown, type: 'create' | 'update' | 'delete') => {
    const parsed = NormalizedErrorSchema.safeParse(e)
    if (parsed.success && parsed.data.type === 'validation') {
      const fieldErrors = parsed.data.fieldErrors
      const summary =
        fieldErrors &&
        Object.entries(fieldErrors)
          .map(([field, msgs]) => `${field}: ${msgs.join(', ')}`)
          .join('; ')
      toast.error(`Failed to ${type} scale plan`, { description: summary })
      return
    }
    if (e instanceof AxiosError) {
      toast.error(`Failed to ${type} scale plan`, {
        description: e.response?.data?.message || e.message || 'An error occurred',
      })
    } else {
      toast.error(`Failed to ${type} scale plan`)
    }
  }

  const handleSuccess = (type: 'create' | 'update' | 'delete') => {
    queryClient.invalidateQueries({ queryKey: liveTradeKeys.all })
    toast.success(`Scale plan ${type}d successfully`)
  }

  const createMutation = useMutation({
    mutationFn: ({ data, liveTradeId }: { data: ScalePlanCreate; liveTradeId: string }) =>
      createScalePlan(liveTradeId, data),
    onSuccess: () => handleSuccess('create'),
    onError: (e) => handleError(e, 'create'),
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: ScalePlanUpdate }) => updateScalePlan(id, data),
    onSuccess: () => handleSuccess('update'),
    onError: (e) => handleError(e, 'update'),
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteScalePlan(id),
    onSuccess: () => handleSuccess('delete'),
    onError: (e) => handleError(e, 'delete'),
  })

  return {
    deleteMutation,
    createMutation,
    updateMutation,
  }
}

export const useScalePlanValidationService = () => {}
