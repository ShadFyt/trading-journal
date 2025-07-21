import { createTradeIdea, getTradeIdeas } from '@/api'
import type { TradeIdeaCreate } from '@/interfaces/trade-idea.type'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'

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
    },
  })

  return {
    createMutation,
  }
}
