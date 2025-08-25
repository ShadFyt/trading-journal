<script setup lang="ts">
import { computed } from 'vue'
import { useMockLiveTrades } from '@/composables/useMockLiveTrades.ts'
import { useFormatters } from '@/composables'

const { getTotalPnL, getTotalPortfolioValue } = useMockLiveTrades()
const { formatCurrency } = useFormatters()

const portfolioStats = computed(() => {
  return {
    totalPnL: getTotalPnL(),
    totalValue: getTotalPortfolioValue(),
    activePositions: 5,
    profitablePositions: 3,
  }
})
</script>

<template>
  <section class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
    <PortfolioCard title="Total P&L">
      <span :class="portfolioStats.totalPnL >= 0 ? 'text-green-600' : 'text-red-600'">
        {{ formatCurrency(portfolioStats.totalPnL) }}
      </span>
    </PortfolioCard>

    <PortfolioCard title="Portfolio Value">
      <span class="text-gray-900">{{ formatCurrency(portfolioStats.totalValue) }}</span>
    </PortfolioCard>

    <PortfolioCard title="Active Positions">
      <span class="text-blue-600">{{ portfolioStats.activePositions }}</span>
    </PortfolioCard>

    <PortfolioCard title="Profitable">
      <span class="text-green-600">
        {{ portfolioStats.profitablePositions }}/{{ portfolioStats.activePositions }}
      </span>
    </PortfolioCard>
  </section>
</template>
