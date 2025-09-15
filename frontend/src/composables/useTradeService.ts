import {
  createTrade,
  deleteTrade,
  getTrades,
  invalidateTrade,
  replaceTrade,
  updateTrade,
} from '@/api/trade.api.ts'
import { useMutation, useQuery, useQueryClient } from '@tanstack/vue-query'
import { toast } from 'vue-sonner'
import { AxiosError } from 'axios'
import type { crudType, TradeCreate, TradeUpdate } from '@/interfaces'
import { handleErrorDisplay } from '@/api/api-error.util.ts'
import { TradeStatusEnum } from '@/enums/trade.enum.ts'

export const liveTradeKeys = {
  all: ['live-trades'] as const,
  list: () => [...liveTradeKeys.all, 'list'] as const,
  detail: (id: string) => [...liveTradeKeys.all, 'detail', id] as const,
}

export const useTradeFetchingService = () => {
  const { data, isLoading, refetch } = useQuery({
    queryKey: liveTradeKeys.list(),
    queryFn: () => getTrades(),
    staleTime: 60 * 60 * 1000, // 1 hour
    refetchOnWindowFocus: true,
  })
  const liveTrades = computed(() => data.value?.filter((trade) => trade.status === 'open') ?? [])
  const watchlist = computed(
    () => data.value?.filter((trade) => trade.status === TradeStatusEnum.enum.WATCHING) ?? [],
  )

  return { liveTrades, isLoading, refetchLiveTrades: refetch, watchlist }
}

export const useTradeMutationService = () => {
  const queryClient = useQueryClient()
  const domain = 'live trade'

  const handleSuccess = (type: crudType, message?: string) => {
    queryClient.invalidateQueries({ queryKey: liveTradeKeys.list() })

    toast.success(message ?? `Live trade ${type}d successfully`)
  }

  const createMutation = useMutation({
    mutationFn: (data: TradeCreate) => createTrade(data),
    onSuccess: () => handleSuccess('create'),
    onError: (e) => handleErrorDisplay(e, 'create', domain),
  })

  const replaceMutation = useMutation<
    Awaited<ReturnType<typeof replaceTrade>>,
    AxiosError,
    { id: string; data: TradeCreate }
  >({
    mutationFn: ({ id, data }) => replaceTrade(id, data),
    onSuccess: () => handleSuccess('update'),
    onError: (e) => handleErrorDisplay(e, 'update', domain),
  })

  const updateMutation = useMutation<
    Awaited<ReturnType<typeof updateTrade>>,
    AxiosError,
    { id: string; data: TradeUpdate; message?: string }
  >({
    mutationFn: ({ id, data }) => updateTrade(id, data),
    onSuccess: (_data, variables) => handleSuccess('update', variables?.message),
    onError: (e) => handleErrorDisplay(e, 'update', domain),
  })

  const deleteMutation = useMutation({
    mutationFn: (id: string) => deleteTrade(id),
    onSuccess: () => handleSuccess('delete'),
    onError: (e) => handleErrorDisplay(e, 'delete', domain),
  })

  const invalidateMutation = useMutation({
    mutationFn: (id: string) => invalidateTrade(id),
    onSuccess: () => handleSuccess('update', 'Trade invalidated successfully'),
    onError: (e) => handleErrorDisplay(e, 'update', domain),
  })

  return { createMutation, updateMutation, deleteMutation, replaceMutation, invalidateMutation }
}
