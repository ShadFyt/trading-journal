import { getTradeIdeas } from '@/api'
import { useQuery } from '@tanstack/vue-query'

export const tradeIdeaKeys = {
  all: ['trade-ideas'] as const,
  list: () => [...tradeIdeaKeys.all, 'list'] as const,
  detail: (id: string) => [...tradeIdeaKeys.all, 'detail', id] as const,
}

export const useTradeIdeaFetchingService = () => {
  const { data: tradeIdeas } = useQuery({
    queryKey: tradeIdeaKeys.list(),
    queryFn: () => getTradeIdeas(),
    staleTime: 60 * 60 * 1000, // 1 hour
    refetchOnWindowFocus: true,
  })

  return {
    tradeIdeas,
  }
}
