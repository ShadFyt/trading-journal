import { createTradeIdea, getTradeIdeas, deleteTradeIdea } from '@/api'
import type { TradeIdeaCreate } from '@/interfaces/trade-idea.type'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { toast } from 'vue-sonner'
import { AxiosError } from 'axios'
import { validationErrorResponseSchema } from '@/api/api-error.util'

/**
 * Trade idea specific field labels
 * Can be used as a reference for other forms
 */
export const tradeIdeaFieldLabels: Record<string, string> = {
  status: 'Status',
  entryMax: 'Entry Max',
  entryMin: 'Entry Min',
  catalysts: 'Catalysts',
  ideaDate: 'Idea Date',
  notes: 'Notes',
  rrRatio: 'Risk/Reward Ratio',
  targetPrices: 'Target Prices',
  symbol: 'Symbol',
  setup: 'Setup Type',
  rating: 'Rating',
  stop: 'Stop Loss',
}

export const tradeIdeaKeys = {
  all: ['trade-ideas'] as const,
  list: () => [...tradeIdeaKeys.all, 'list'] as const,
  detail: (id: string) => [...tradeIdeaKeys.all, 'detail', id] as const,
}

export const useTradeIdeaFetchingService = () => {
  const { data: tradeIdeas, isLoading } = useQuery({
    queryKey: tradeIdeaKeys.list(),
    queryFn: () => getTradeIdeas(),
    staleTime: 60 * 60 * 1000, // 1 hour
    refetchOnWindowFocus: true,
  })

  return {
    tradeIdeas,
    isLoading,
  }
}

export const useTradeIdeaMutationService = () => {
  const queryClient = useQueryClient()
  const createMutation = useMutation({
    mutationFn: (data: TradeIdeaCreate) => createTradeIdea(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: tradeIdeaKeys.list() })
      toast.success('Trade idea created successfully')
    },
    onError: (e) => {
      if (e instanceof AxiosError) {
        console.error('axios error', e.response?.data)

        // Handle validation errors (422 status)
        console.info('axios status', e.response?.status)
        if (e.response?.status === 422) {
          try {
            const validationErrors = validationErrorResponseSchema.parse(e.response.data.detail)
            const errorCount = validationErrors.length
            const firstError = validationErrors[0]
            const fieldName = firstError.loc.slice(1).join('.')
            const fieldLabel = tradeIdeaFieldLabels[fieldName] || fieldName

            let message: string
            if (errorCount === 1) {
              message = `${fieldLabel}: ${firstError.msg}`
            } else {
              message = `${fieldLabel} and ${errorCount - 1} other field${errorCount > 2 ? 's' : ''} required`
            }

            console.info('Validation failed:', message)
            toast.error(message)
            return
          } catch (parseError) {
            console.error('Failed to parse validation errors:', parseError)
            toast.error('Failed to create trade idea')
          }
        }

        // Handle other HTTP errors
        const errorMessage = e.response?.data?.message || e.message || 'An error occurred'
        toast.error(`Failed to create trade idea: ${errorMessage}`)
      } else {
        toast.error('Failed to create trade idea')
      }
    },
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteTradeIdea(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: tradeIdeaKeys.list() })
      toast.success('Trade idea deleted successfully')
    },
    onError: (e) => {
      if (e instanceof AxiosError) {
        const errorMessage = e.response?.data?.message || e.message || 'An error occurred'
        toast.error(`Failed to delete trade idea: ${errorMessage}`)
      } else {
        toast.error('Failed to delete trade idea')
      }
    },
  })

  return {
    createMutation,
    deleteMutation,
  }
}
