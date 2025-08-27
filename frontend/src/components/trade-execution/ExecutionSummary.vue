<script lang="ts" setup>
import type { ExecutionDto } from '@/interfaces'
import { useFormatters } from '@/composables'
import InfoWrapper from '@/components/trade-execution/InfoWrapper.vue'
const { formatCurrency, formatPercentage } = useFormatters()

const { executions, entryPriceAvg, targetPrice, stop } = defineProps<{
  executions: ExecutionDto[]
  entryPriceAvg: number
  targetPrice?: number
  stop: number
}>()

const avgFillPrice = computed(() => {
  const total = executions.reduce((total, exec) => total + exec.price * exec.qty, 0)
  const qty = executions.reduce((total, exec) => total + exec.qty, 0)
  if (qty === 0) return null
  return total / qty
})

// Long-only realized metrics: consider SELL executions only
const soldQty = computed(() =>
  executions.filter((e) => e.side === 'sell').reduce((t, e) => t + e.qty, 0),
)

const realizedPnL = computed(() =>
  executions
    .filter((e) => e.side === 'sell')
    .reduce((t, e) => t + (e.price - entryPriceAvg) * e.qty - e.commission, 0),
)

const realizedPct = computed(() =>
  soldQty.value > 0 ? (realizedPnL.value / (entryPriceAvg * soldQty.value)) * 100 : null,
)

const realizedR = computed(() => {
  const hasQty = soldQty.value > 0
  const riskPerShare = entryPriceAvg - stop
  const validRisk = riskPerShare != null && riskPerShare > 0
  if (!hasQty || !validRisk) return null
  return realizedPnL.value / ((riskPerShare as number) * soldQty.value)
})

const slippageAbs = computed(() => {
  const has = avgFillPrice.value != null
  return has ? (avgFillPrice.value as number) - (targetPrice as number) : null
})

const slippagePct = computed(() => {
  const valid = avgFillPrice.value != null && targetPrice! > 0
  return valid
    ? (((avgFillPrice.value as number) - (targetPrice as number)) / (targetPrice as number)) * 100
    : null
})

const posNegClass = (v?: number | null, neutral = 'text-gray-700') =>
  v == null ? neutral : v >= 0 ? 'text-emerald-700' : 'text-rose-700'
</script>

<template>
  <div class="grid grid-cols-2 gap-2 text-sm mt-2">
    <InfoWrapper v-if="avgFillPrice != null" title="Avg Fill Price">
      {{ (realizedR as number).toFixed(2) }}{{ formatCurrency(avgFillPrice) }}
    </InfoWrapper>

    <InfoWrapper title="Realized PnL" :extra-classes="posNegClass(realizedPnL)">
      {{ formatCurrency(realizedPnL) }}
      <span class="ml-1 text-xs" :class="realizedPnL >= 0 ? 'text-emerald-700' : 'text-rose-700'">
        ({{ realizedPct != null ? formatPercentage(realizedPct) : '' }})
      </span>
    </InfoWrapper>

    <InfoWrapper title="Slippage vs Target" :extra-classes="posNegClass(slippageAbs)">
      {{ formatCurrency(slippageAbs as number) }}
      <span
        class="ml-1 text-xs"
        :class="(slippageAbs as number) >= 0 ? 'text-emerald-700' : 'text-rose-700'"
      >
        ({{ slippagePct != null ? formatPercentage(slippagePct as number) : '' }})
      </span>
    </InfoWrapper>

    <InfoWrapper title="Realized R" :extra-classes="posNegClass(realizedPnL)">
      {{ (realizedR as number).toFixed(2) }}R
    </InfoWrapper>
  </div>
</template>
