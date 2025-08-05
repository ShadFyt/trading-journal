<script setup lang="ts">
import { computed } from 'vue'
import LiveTradeCard from './LiveTradeCard.vue'
import { useMockLiveTrades } from '@/composables/useMockLiveTrades'
import { useFormatters } from '@/composables'

const { getActiveTrades, getTotalPnL, getTotalPortfolioValue } = useMockLiveTrades()
const { formatCurrency } = useFormatters()

/**
 * Get only active trades for display
 */
const activeTrades = computed(() => getActiveTrades())

/**
 * Portfolio summary stats
 */
const portfolioStats = computed(() => ({
  totalPnL: getTotalPnL(),
  totalValue: getTotalPortfolioValue(),
  activePositions: activeTrades.value.length,
  profitablePositions: 3,
}))

/**
 * Handle trade management actions
 */
const handleAdjustStop = (tradeId: string, type: 'breakeven' | 'trailing') => {
  console.log(`Adjusting stop for ${tradeId} to ${type}`)
  // Implementation would go here
}

const handlePartialExit = (tradeId: string, percentage: number) => {
  console.log(`Partial exit ${percentage}% for trade ${tradeId}`)
  // Implementation would go here
}

const handleAddPosition = (tradeId: string) => {
  console.log(`Adding to position ${tradeId}`)
  // Implementation would go here
}

const handleCloseTrade = (tradeId: string) => {
  console.log(`Closing trade ${tradeId}`)
  // Implementation would go here
}

const handleEditTrade = (tradeId: string) => {
  console.log(`Editing trade ${tradeId}`)
  // Implementation would go here
}
</script>

<template>
  <main class="p-4 max-w-7xl mx-auto">
    <!-- Header -->
    <header class="mb-6">
      <h1 class="text-3xl font-bold text-gray-900 mb-2">Live Trades</h1>

      <!-- Portfolio Summary -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
          <p class="text-xs text-gray-600 uppercase tracking-wide">Total P&L</p>
          <p
            class="text-2xl font-bold"
            :class="portfolioStats.totalPnL >= 0 ? 'text-green-600' : 'text-red-600'"
          >
            {{ formatCurrency(portfolioStats.totalPnL) }}
          </p>
        </div>

        <div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
          <p class="text-xs text-gray-600 uppercase tracking-wide">Portfolio Value</p>
          <p class="text-2xl font-bold text-gray-900">
            {{ formatCurrency(portfolioStats.totalValue) }}
          </p>
        </div>

        <div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
          <p class="text-xs text-gray-600 uppercase tracking-wide">Active Positions</p>
          <p class="text-2xl font-bold text-blue-600">
            {{ portfolioStats.activePositions }}
          </p>
        </div>

        <div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
          <p class="text-xs text-gray-600 uppercase tracking-wide">Profitable</p>
          <p class="text-2xl font-bold text-green-600">
            {{ portfolioStats.profitablePositions }}/{{ portfolioStats.activePositions }}
          </p>
        </div>
      </div>
    </header>

    <!-- Live Trades Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <LiveTradeCard
        v-for="trade in activeTrades"
        :key="trade.id"
        :trade="trade"
        @adjust-stop="handleAdjustStop"
        @partial-exit="handlePartialExit"
        @add-position="handleAddPosition"
        @close-trade="handleCloseTrade"
        @edit-trade="handleEditTrade"
      />
    </div>

    <!-- Empty State -->
    <div v-if="activeTrades.length === 0" class="text-center py-12">
      <div class="text-6xl mb-4">📈</div>
      <h3 class="text-xl font-semibold text-gray-900 mb-2">No Active Trades</h3>
      <p class="text-gray-600">
        Your live trades will appear here once you convert trade ideas to positions.
      </p>
    </div>
  </main>
</template>
