<script setup lang="ts">
import type { LiveTrade } from '@/interfaces'
import { useFormatters } from '@/composables'
import InfoWrapper from '@/components/live-trades/portfolio/InfoWrapper.vue'

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
    <InfoWrapper :title="'Current Price'" :is-green="trade.currentPrice >= trade.entryPriceAvg">
      {{ formatCurrency(trade.currentPrice) }}
    </InfoWrapper>

    <!-- Profit/Loss -->
    <InfoWrapper :title="'Profit/Loss'" :is-green="pnl >= 0">
      {{ (pnl >= 0 ? '+' : '') + formatCurrency(pnl) }}
    </InfoWrapper>

    <!-- Percentage -->
    <InfoWrapper :title="'Percentage'" :is-green="pnl >= 0">
      {{
        formatPercentage(((trade.currentPrice - trade.entryPriceAvg) / trade.entryPriceAvg) * 100)
      }}
    </InfoWrapper>
  </section>
</template>
