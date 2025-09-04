<script setup lang="ts">
import type { LiveTrade, ScalePlan } from '@/interfaces'
import { useFormatters, useTradeMetrics } from '@/composables'

const { trade, plan } = defineProps<{
  trade: LiveTrade
  plan: ScalePlan
}>()
const { initialPosition, entryPrice } = useTradeMetrics(trade)

const { formatCurrency } = useFormatters()

const isFiniteNumber = (v: unknown): v is number => {
  return typeof v === 'number' && Number.isFinite(v)
}

const computeEffectiveShares = (baseShares: number, value: unknown): number | null => {
  return isFiniteNumber(value) ? value : null
}

const projectedPnLAtTarget = computed(() => {
  if (entryPrice == null || plan.targetPrice == null) return null

  const baseShares = initialPosition
  const effectiveShares = computeEffectiveShares(baseShares, plan.qty)
  if (!effectiveShares || effectiveShares <= 0) return null

  const isLong = true // TODO: infer from side/orderType
  const delta = isLong ? plan.targetPrice - entryPrice : entryPrice - plan.targetPrice
  return delta * effectiveShares
})

const projectedReturnPct = computed(() => {
  if (entryPrice == null || entryPrice === 0 || plan.targetPrice == null) return null
  const isLong = true

  const delta = isLong ? plan.targetPrice - entryPrice : entryPrice - plan.targetPrice
  return (delta / entryPrice) * 100
})

const pnlPercentBadgeClass = computed(() => {
  const v = Number(projectedReturnPct.value ?? NaN)
  if (!Number.isFinite(v)) return 'bg-gray-100 text-gray-800'
  if (v <= -5) return 'bg-red-100 text-red-800'
  if (v < -1) return 'bg-orange-100 text-orange-800'
  if (v < 1) return 'bg-gray-100 text-gray-800'
  if (v < 5) return 'bg-yellow-100 text-yellow-800'
  if (v < 10) return 'bg-green-100 text-green-800'
  return 'bg-emerald-100 text-emerald-800'
})
</script>

<template>
  <div class="grid grid-cols-2 gap-2 text-sm mt-2">
    <div v-if="plan.targetPrice != null" class="rounded bg-gray-50 p-2">
      <p class="text-xs text-gray-600">Target</p>
      <p class="font-medium">{{ formatCurrency(plan.targetPrice) }}</p>
    </div>

    <div v-if="projectedPnLAtTarget != null" class="rounded bg-gray-50 p-2">
      <p class="text-xs text-gray-600">Projected P&amp;L (target)</p>
      <p class="font-medium">
        {{ formatCurrency(projectedPnLAtTarget) }}
        <span
          v-if="projectedReturnPct != null"
          class="text-xs text-gray-600 rounded-full px-2 py-0.5"
          :class="pnlPercentBadgeClass"
          :aria-label="`Projected return ${projectedReturnPct.toFixed(2)}% at target`"
        >
          ({{ projectedReturnPct.toFixed(2) }}%)
        </span>
      </p>
    </div>
  </div>
</template>
