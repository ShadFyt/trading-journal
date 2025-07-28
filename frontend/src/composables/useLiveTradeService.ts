import { createLiveTrade, getLiveTrades } from '@/api/live-trade.api'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { toast } from 'vue-sonner'
import { AxiosError } from 'axios'
import type { LiveTradeCreate } from '@/interfaces'
import { tradeIdeaKeys } from '@/composables/useTradeIdeaService'

export const liveTradeKeys = {
  all: ['live-trades'] as const,
  list: () => [...liveTradeKeys.all, 'list'] as const,
  detail: (id: string) => [...liveTradeKeys.all, 'detail', id] as const,
}

export const useLiveTradeFetchingService = () => {
  const { data: liveTrades, isLoading } = useQuery({
    queryKey: liveTradeKeys.list(),
    queryFn: () => getLiveTrades(),
    staleTime: 60 * 60 * 1000, // 1 hour
    refetchOnWindowFocus: true,
  })

  return { liveTrades, isLoading }
}

export const useLiveTradeMutationService = () => {
  const queryClient = useQueryClient()
  const createMutation = useMutation({
    mutationFn: (data: LiveTradeCreate) => createLiveTrade(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: liveTradeKeys.list() })
      queryClient.invalidateQueries({ queryKey: tradeIdeaKeys.list() })

      toast.success('Live trade created successfully')
    },
    onError: (e) => {
      if (e instanceof AxiosError) {
        const errorMessage = e.response?.data?.message || e.message || 'An error occurred'
        toast.error(`Failed to create live trade: ${errorMessage}`)
      } else {
        toast.error('Failed to create live trade')
      }
    },
  })

  return { createMutation }
}
