import type { InjectionKey } from 'vue'
import type { Trade } from '@/interfaces'
import { ScalePlanStatusEnum, ScalePlanTypeEnum, ScaleTradeTypeEnum } from '@/enums'

type TradeType = 'long' | 'short'

type EntryPlanMetrics = {
  entryPriceAvg: number
  qty: number
  stopLoss: number
  tradeType: TradeType
}

export const useTradeMetrics = (trade: Trade) => {
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

  const createEntryPlanMetrics = (
    entryPriceAvg: number,
    qty: number,
    stopLoss: number,
    tradeType: TradeType,
  ): EntryPlanMetrics => ({
    entryPriceAvg,
    qty,
    stopLoss,
    tradeType,
  })

  // Helper to get default trade type
  const getDefaultTradeType = (plan?: any): TradeType =>
    plan?.tradeType ?? ScaleTradeTypeEnum.enum.LONG

  const latestStopLossPlan = computed(() => {
    return trade.scalePlans.find(
      (plan) =>
        plan.planType === ScalePlanTypeEnum.enum.STOP_LOSS &&
        plan.status !== ScalePlanStatusEnum.enum.CANCELLED,
    )
  })

  const entryPlan = computed((): EntryPlanMetrics => {
    const plan = trade.scalePlans.find(
      (plan) =>
        plan.planType === ScalePlanTypeEnum.enum.ENTRY &&
        (plan.status === ScalePlanStatusEnum.enum.FILLED ||
          plan.status === ScalePlanStatusEnum.enum.PLANNED),
    )

    const defaultStopLoss = latestStopLossPlan.value?.stopPrice ?? 0
    const tradeType = getDefaultTradeType(plan)

    // Handle planned entry (not yet executed)
    if (plan?.status === ScalePlanStatusEnum.enum.PLANNED) {
      return createEntryPlanMetrics(
        plan.limitPrice ?? 0,
        plan.qty ?? 0,
        plan.stopPrice ?? 0,
        tradeType,
      )
    }

    // Handle missing plan or no executions
    if (!plan?.executions?.length) {
      return createEntryPlanMetrics(0, 0, defaultStopLoss, tradeType)
    }

    // Handle executed entry plan
    const totalQty = plan.executions.reduce((sum, exec) => sum + exec.qty, 0)
    const avgPrice = calculateWeightedAvgPrice(plan.executions)
    const stopLoss = (defaultStopLoss || plan.stopPrice) ?? 0

    return createEntryPlanMetrics(avgPrice, totalQty, stopLoss, tradeType)
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
    executions,
    trade,
    entryPlan,
  }
}

export type TradeMetricsType = ReturnType<typeof useTradeMetrics>
export const TRADE_METRICS_KEY: InjectionKey<TradeMetricsType> = Symbol('tradeMetrics')

export const useInjectTradeMetrics = (): TradeMetricsType => {
  const tradeMetrics = inject(TRADE_METRICS_KEY)

  if (!tradeMetrics) {
    throw new Error('Trade metrics not provided. Make sure to wrap component with trade provider.')
  }

  return tradeMetrics
}
