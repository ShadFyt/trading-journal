import { toast } from 'vue-sonner'
import { AxiosError } from 'axios'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { liveTradeKeys } from '@/composables/useLiveTradeService.ts'
import { deleteScalePlan } from '@/api/scale-plan.api.ts'

export const scalePlanKeys = {
  all: () => ['scalePlan'],
  list: () => [...scalePlanKeys.all(), 'list'],
  trade: (id: string) => [...scalePlanKeys.all(), 'trade', id],
  detail: (id: string) => [...scalePlanKeys.all(), 'detail', id],
} as const

export const useScalePlanMutationService = () => {
  const queryClient = useQueryClient()
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
  }
}
