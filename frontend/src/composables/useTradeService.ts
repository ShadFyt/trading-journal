import {
  createLiveTrade,
  deleteLiveTrade,
  getLiveTrades,
  updateLiveTrade,
} from '@/api/trade.api.ts'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { toast } from 'vue-sonner'
import { AxiosError } from 'axios'
import type { crudType, LiveTradeCreate, LiveTradeUpdate } from '@/interfaces'
import { handleErrorDisplay } from '@/api/api-error.util.ts'
import { TradeStatusEnum } from '@/enums/trade.enum.ts'

export const liveTradeKeys = {
  all: ['live-trades'] as const,
  list: () => [...liveTradeKeys.all, 'list'] as const,
  detail: (id: string) => [...liveTradeKeys.all, 'detail', id] as const,
}

export const useLiveTradeFetchingService = () => {
  const { data, isLoading, refetch } = useQuery({
    queryKey: liveTradeKeys.list(),
    queryFn: () => getLiveTrades(),
    staleTime: 60 * 60 * 1000, // 1 hour
    refetchOnWindowFocus: true,
  })
  const liveTrades = computed(() => data.value?.filter((trade) => trade.status === 'open') ?? [])
  const watchlist = computed(
    () => data.value?.filter((trade) => trade.status === TradeStatusEnum.enum.WATCHING) ?? [],
  )

  return { liveTrades, isLoading, refetchLiveTrades: refetch, watchlist }
}

export const useLiveTradeMutationService = () => {
  const queryClient = useQueryClient()
  const domain = 'live trade'

  const handleSuccess = (type: crudType, message?: string) => {
    queryClient.invalidateQueries({ queryKey: liveTradeKeys.list() })

    toast.success(message ?? `Live trade ${type}d successfully`)
  }

  const createMutation = useMutation({
    mutationFn: (data: LiveTradeCreate) => createLiveTrade(data),
    onSuccess: () => handleSuccess('create'),
    onError: (e) => handleErrorDisplay(e, 'create', domain),
  })

  const updateMutation = useMutation<
    Awaited<ReturnType<typeof updateLiveTrade>>,
    AxiosError,
    { id: string; data: LiveTradeUpdate; message?: string }
  >({
    mutationFn: ({ id, data }) => updateLiveTrade(id, data),
    onSuccess: (_data, variables) => handleSuccess('update', variables?.message),
    onError: (e) => handleErrorDisplay(e, 'update', domain),
  })
  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteLiveTrade(id),
    onSuccess: () => handleSuccess('delete'),
    onError: (e) => handleErrorDisplay(e, 'delete', domain),
  })

  return { createMutation, updateMutation, deleteMutation }
}
