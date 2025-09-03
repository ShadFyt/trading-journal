import type { LiveTrade } from '@/interfaces'
import { ScalePlanStatusEnum, ScalePlanTypeEnum } from '@/enums'

export const useTradeMetrics = (trade: LiveTrade) => {
  const executions = computed(() =>
    trade.scalePlans
      .filter((plan) => plan.planType === ScalePlanTypeEnum.enum.TARGET)
      .flatMap((plan) => plan.executions),
  )
  const soldShares = computed(() => executions.value.reduce((total, exec) => total + exec.qty, 0))
  // Helper to calculate weighted average price from executions
  const calculateWeightedAvgPrice = (executions: Array<{ price: number; qty: number }>) => {
    if (executions.length === 0) return 0

    const totalQty = executions.reduce((sum, exec) => sum + exec.qty, 0)
    if (totalQty === 0) return 0

    const totalValue = executions.reduce((sum, exec) => sum + exec.price * exec.qty, 0)
    return totalValue / totalQty
  }

  const latestStopLossPlan = computed(() => {
    return trade.scalePlans.find(
      (plan) =>
        plan.planType === ScalePlanTypeEnum.enum.STOP_LOSS &&
        plan.status !== ScalePlanStatusEnum.enum.CANCELLED,
    )
  })

  const entryPlan = computed(() => {
    const plan = trade.scalePlans.find(
      (plan) =>
        plan.planType === ScalePlanTypeEnum.enum.ENTRY &&
        plan.status === ScalePlanStatusEnum.enum.FILLED,
    )

    if (!plan?.executions?.length) {
      return {
        entryPriceAvg: 0,
        qty: 0,
        stopLoss: latestStopLossPlan.value?.stopPrice ?? 0,
      }
    }

    const totalQty = plan.executions.reduce((sum, exec) => sum + exec.qty, 0)
    const avgPrice = calculateWeightedAvgPrice(plan.executions)

    return {
      entryPriceAvg: avgPrice,
      qty: totalQty,
      stopLoss: latestStopLossPlan.value?.stopPrice ?? plan.stopPrice ?? 0,
    }
  })

  const realizedPnL = computed(() => {
    const commissions = executions.value.reduce((total, exec) => total + (exec.commission ?? 0), 0)
    const entryPriceAvg = entryPlan.value.entryPriceAvg
    const grossPnL = executions.value.reduce(
      (total, exec) => total + (exec.price - entryPriceAvg) * exec.qty,
      0,
    )
    return grossPnL - commissions
  })
  const realizedPct = computed(() => {
    if (realizedPnL.value === 0 || soldShares.value === 0) return 0
    const entryValue = entryPlan.value.entryPriceAvg * soldShares.value
    return (realizedPnL.value / entryValue) * 100
  })

  const remainingShares = computed(() => Math.max(entryPlan.value.qty - soldShares.value, 0))

  const unrealizedPnL = computed(() => {
    if (remainingShares.value <= 0) return 0
    return (trade.currentPrice - entryPlan.value.entryPriceAvg) * remainingShares.value
  })

  const unrealizedPct = computed(() => {
    if (remainingShares.value <= 0) return 0
    const entryValue = entryPlan.value.entryPriceAvg * remainingShares.value
    return (unrealizedPnL.value / entryValue) * 100
  })

  const totalPnL = computed(() => realizedPnL.value + unrealizedPnL.value)
  const totalPct = computed(() => {
    if (entryPlan.value.qty === 0) return 0
    const entryValue = entryPlan.value.entryPriceAvg * entryPlan.value.qty
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
    entryPrice: entryPlan.value.entryPriceAvg,
    initialPosition: entryPlan.value.qty,
    stopLoss: entryPlan.value.stopLoss,
  }
}
