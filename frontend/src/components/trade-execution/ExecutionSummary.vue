<script lang="ts" setup>
import type { ExecutionDto } from '@/interfaces'
import { useFormatters } from '@/composables'
const { formatCurrency, formatPercentage } = useFormatters()

const { executions, entryPriceAvg, targetPrice } = defineProps<{
  executions: ExecutionDto[]
  entryPriceAvg: number
  targetPrice?: number
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
</script>

<template>
  <div class="grid grid-cols-2 gap-2 text-sm mt-2">
    <div v-if="avgFillPrice != null" class="rounded bg-gray-50 p-2">
      <p class="text-xs text-gray-600">Avg Fill Price</p>
      <p class="font-medium">{{ formatCurrency(avgFillPrice) }}</p>
    </div>

    <div v-if="soldQty > 0" class="rounded bg-gray-50 p-2">
      <p class="text-xs text-gray-600">Realized PnL</p>
      <p class="font-medium" :class="realizedPnL >= 0 ? 'text-emerald-700' : 'text-rose-700'">
        {{ formatCurrency(realizedPnL) }}
        <span class="ml-1 text-xs" :class="realizedPnL >= 0 ? 'text-emerald-700' : 'text-rose-700'">
          ({{ realizedPct != null ? formatPercentage(realizedPct) : '' }})
        </span>
      </p>
    </div>

    <div v-if="slippageAbs != null" class="rounded bg-gray-50 p-2">
      <p class="text-xs text-gray-600">Slippage vs Target</p>
      <p
        class="font-medium"
        :class="(slippageAbs as number) >= 0 ? 'text-emerald-700' : 'text-rose-700'"
      >
        {{ formatCurrency(slippageAbs as number) }}
        <span
          class="ml-1 text-xs"
          :class="(slippageAbs as number) >= 0 ? 'text-emerald-700' : 'text-rose-700'"
        >
          ({{ slippagePct != null ? formatPercentage(slippagePct as number) : '' }})
        </span>
      </p>
    </div>
  </div>
</template>
