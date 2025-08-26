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
    class="grid grid-cols-1 gap-3 sm:grid-cols-3 p-3 rounded-lg mb-3 border"
    :class="[pnlStyling.bgColor, pnlStyling.borderColor]"
  >
    <!-- Current Price -->
    <div class="flex sm:flex-col justify-between sm:justify-between sm:h-full">
      <p class="text-xs text-gray-600 uppercase tracking-wide">Current Price</p>
      <span
        class="text-base font-bold sm:mt-1 sm:text-xl"
        :class="trade.currentPrice >= trade.entryPriceAvg ? 'text-green-600' : 'text-red-600'"
        aria-live="polite"
        aria-atomic="true"
      >
        {{ formatCurrency(trade.currentPrice) }}
      </span>
    </div>

    <!-- Profit/Loss -->
    <div class="flex sm:flex-col justify-between sm:justify-between sm:h-full">
      <p class="text-xs text-gray-600 uppercase tracking-wide">Profit/Loss</p>
      <span
        class="text-base font-bold sm:mt-1 sm:text-2xl"
        :class="pnl >= 0 ? 'text-green-600' : 'text-red-600'"
        aria-live="polite"
        aria-atomic="true"
      >
        {{ (pnl >= 0 ? '+' : '') + formatCurrency(pnl) }}
      </span>
    </div>

    <!-- Percentage -->
    <div class="flex sm:flex-col justify-between sm:justify-between sm:h-full sm:text-right">
      <p class="text-xs text-gray-600 uppercase tracking-wide">Percentage</p>
      <span
        class="text-sm sm:mt-1 sm:text-base"
        :class="pnl >= 0 ? 'text-green-600' : 'text-red-600'"
        aria-live="polite"
        aria-atomic="true"
      >
        {{
          formatPercentage(((trade.currentPrice - trade.entryPriceAvg) / trade.entryPriceAvg) * 100)
        }}
      </span>
    </div>
  </section>
</template>
