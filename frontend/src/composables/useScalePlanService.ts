import { toast } from 'vue-sonner'
import { AxiosError } from 'axios'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { liveTradeKeys } from '@/composables/useLiveTradeService.ts'
import { createScalePlan, deleteScalePlan } from '@/api/scale-plan.api.ts'
import type { ScalePlanCreate } from '@/interfaces'

export const scalePlanKeys = {
  all: ['scalePlan'] as const,
  list: () => [...scalePlanKeys.all, 'list'] as const,
  trade: (id: string) => [...scalePlanKeys.all, 'trade', id] as const,
  detail: (id: string) => [...scalePlanKeys.all, 'detail', id] as const,
}

export const useScalePlanMutationService = () => {
  const queryClient = useQueryClient()

  const createMutation = useMutation({
    mutationFn: ({ data, liveTradeId }: { data: ScalePlanCreate; liveTradeId: string }) =>
      createScalePlan(liveTradeId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: liveTradeKeys.all })
      toast.success('Scale plan created successfully')
    },
    onError: (e: unknown) => {
      if (e instanceof AxiosError) {
        toast.error(
          `Failed to create scale plan: ${e.response?.data?.message || e.message || 'An error occurred'}`,
        )
      } else {
        toast.error('Failed to create scale plan')
      }
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteScalePlan(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: liveTradeKeys.all })
      toast.success('Scale plan deleted successfully')
    },
    onError: (e: unknown) => {
      if (e instanceof AxiosError) {
        toast.error(
          `Failed to delete scale plan: ${e.response?.data?.message || e.message || 'An error occurred'}`,
        )
      } else {
        toast.error('Failed to delete scale plan')
      }
    },
  })

  return {
    deleteMutation,
    createMutation,
  }
}
