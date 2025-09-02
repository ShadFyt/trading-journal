import type { LiveTrade } from '@/interfaces'

export const useTradeMetrics = (trade: LiveTrade) => {
  const { executions } = trade
  const soldShares = computed(() => executions.reduce((total, exec) => total + exec.qty, 0))
  const realizedPnL = computed(() => {
    const commissions = executions.reduce((total, exec) => total + exec.commission, 0)
    const entryPriceAvg = trade.entryPriceAvg
    const grossPnL = executions.reduce(
      (total, exec) => total + (exec.price - entryPriceAvg) * exec.qty,
      0,
    )
    return grossPnL - commissions
  })
  const realizedPct = computed(() => {
    const entryValue = trade.entryPriceAvg * soldShares.value
    return (realizedPnL.value / entryValue) * 100
  })

  const remainingShares = computed(() => Math.max((trade.positionSize ?? 0) - soldShares.value, 0))
  const unrealizedPnL = computed(
    () => (trade.currentPrice - trade.entryPriceAvg) * remainingShares.value,
  )
  const unrealizedPct = computed(() => {
    if (remainingShares.value <= 0) return 0
    const entryValue = trade.entryPriceAvg * remainingShares.value
    return (unrealizedPnL.value / entryValue) * 100
  })

  const totalPnL = computed(() => realizedPnL.value + unrealizedPnL.value)
  const totalPct = computed(() => {
    const entryValue = trade.entryPriceAvg * trade.positionSize
    return (totalPnL.value / entryValue) * 100
  })
  return {
    soldShares,
    remainingShares,
    realizedPnL,
    realizedPct,
    unrealizedPnL,
    unrealizedPct,
    totalPnL,
    totalPct,
  }
}
