<script setup lang="ts">
import type { LiveTrade } from '@/interfaces'
import { useFormatters } from '@/composables'

const { trade, pnl } = defineProps<{
  trade: LiveTrade
  pnl: number
}>()

const { formatCurrency, formatPercentage } = useFormatters()

/**
 * P&L styling based on profit/loss
 */
const pnlStyling = computed(() => {
  const isProfit = pnl >= 0
  return {
    textColor: isProfit ? 'text-green-600' : 'text-red-600',
    bgColor: isProfit ? 'bg-green-50' : 'bg-red-50',
    borderColor: isProfit ? 'border-green-200' : 'border-red-200',
  }
})
</script>

<template>
  <section
    class="grid grid-cols-1 gap-2 md:grid-cols-3 md:items-center p-3 rounded-lg mb-3 border"
    :class="[pnlStyling.bgColor, pnlStyling.borderColor]"
  >
    <div>
      <p class="text-xs text-gray-600 uppercase tracking-wide">Current Price</p>
      <span
        class="text-lg md:text-xl font-bold"
        :class="trade.currentPrice >= trade.entryPriceAvg ? 'text-green-600' : 'text-red-600'"
        aria-live="polite"
        aria-atomic="true"
      >
        {{ formatCurrency(trade.currentPrice) }}
        <span class="sr-only">
          {{ trade.currentPrice >= trade.entryPriceAvg ? 'above entry' : 'below entry' }}
        </span>
      </span>
    </div>
    <div>
      <p class="text-xs text-gray-600 uppercase tracking-wide">Profit/Loss</p>
      <span
        class="text-xl md:text-2xl font-bold"
        :class="pnl >= 0 ? 'text-green-600' : 'text-red-600'"
        aria-live="polite"
        aria-atomic="true"
      >
        {{ (pnl >= 0 ? '+' : '') + formatCurrency(pnl) }}
      </span>
    </div>
    <div class="md:text-right">
      <p class="text-xs text-gray-600 uppercase tracking-wide">Percentage</p>
      <span
        class="text-sm"
        :class="pnl >= 0 ? 'text-green-600' : 'text-red-600'"
        aria-live="polite"
        aria-atomic="true"
        >{{
          formatPercentage(((trade.currentPrice - trade.entryPriceAvg) / trade.entryPriceAvg) * 100)
        }}</span
      >
    </div>
  </section>
</template>
