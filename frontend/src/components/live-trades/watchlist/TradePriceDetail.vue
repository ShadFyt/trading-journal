<script lang="ts" setup>
import type { Trade } from '@/interfaces'
import { useFormatters, useTradeMetrics } from '@/composables'
import { ScaleTradeTypeEnum } from '@/enums'
const { formatCurrency, formatPercentage } = useFormatters()

const { trade } = defineProps<{
  trade: Trade
}>()

const { entryPrice, entryPlan } = useTradeMetrics(trade)

const isLong = computed(() => entryPlan.value.tradeType === ScaleTradeTypeEnum.enum.LONG)

const tradeTypeBadgeClass = computed(() => {
  const baseClasses = 'rounded-full uppercase'

  return isLong
    ? `${baseClasses} bg-green-100 text-green-700 border border-green-200`
    : `${baseClasses} bg-red-100 text-red-700 border border-red-200`
})
</script>

<template>
  <div class="flex items-center justify-between mb-1">
    <div class="flex items-center gap-2">
      <span class="font-semibold text-white text-sm">{{ trade.symbol }}</span>
      <Badge :class="tradeTypeBadgeClass">
        {{ entryPlan.tradeType }}
      </Badge>
    </div>
    <TradeActionMenu :trade="trade" />
  </div>

  <div class="flex justify-between items-center mb-1">
    <span class="text-white font-medium">Last Price: {{ formatCurrency(trade.currentPrice) }}</span>
    <span
      v-if="trade.percentChange != null"
      class="text-xs"
      :class="trade.percentChange < 0 ? 'text-red-400' : 'text-green-400'"
      >{{ formatPercentage(trade.percentChange) }}</span
    >
  </div>

  <div class="flex justify-between text-xs text-gray-400">
    <span>Entry Target: {{ formatCurrency(entryPrice) }}</span>
    <RatingBadge :rating="trade.rating" />
  </div>
</template>
