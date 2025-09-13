<script setup lang="ts">
import { useFormatters, useInjectTradeMetrics } from '@/composables'

import InfoWrapper from '@/components/live-trades/portfolio/InfoWrapper.vue'

const { realizedPnL, realizedPct, unrealizedPnL, totalPnL, unrealizedPct, entryPrice, trade } =
  useInjectTradeMetrics()

const { formatCurrency, formatPercentage } = useFormatters()

/**
 * P&L styling based on profit/loss
 */
const pnlStyling = computed(() => {
  const isProfit = totalPnL.value >= 0
  return {
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
    <InfoWrapper :title="'Last Price'" :is-green="trade.currentPrice >= entryPrice">
      {{ formatCurrency(trade.currentPrice) }}
    </InfoWrapper>

    <InfoWrapper :title="'Realized PnL'" :is-green="realizedPnL > 0">
      {{ (realizedPnL >= 0 ? '+' : '') + formatCurrency(realizedPnL) }}
      <p class="text-xs ml-5" :class="realizedPnL > 0 ? 'text-emerald-700' : 'text-rose-700'">
        ({{ realizedPct != null ? formatPercentage(realizedPct) : '' }})
      </p>
    </InfoWrapper>

    <InfoWrapper :title="'Unrealized PnL'" :is-green="unrealizedPnL > 0">
      {{ (unrealizedPnL >= 0 ? '+' : '') + formatCurrency(unrealizedPnL) }}
      <p class="text-xs ml-5" :class="unrealizedPnL > 0 ? 'text-emerald-700' : 'text-rose-700'">
        ({{ realizedPct != null ? formatPercentage(unrealizedPct) : '' }})
      </p>
    </InfoWrapper>
  </section>
</template>
