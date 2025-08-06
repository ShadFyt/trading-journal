<script setup lang="ts">
import LiveTradeCard from './LiveTradeCard.vue'
import { useLiveTradeFetchingService } from '@/composables'
import PortfolioSummary from './PortfolioSummary.vue'
import DataRefreshTimer from './DataRefreshTimer.vue'

const { liveTrades: activeTrades, refetchLiveTrades } = useLiveTradeFetchingService()

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
    <header class="mb-">
      <div class="flex justify-between items-center mb-2">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Live Trades</h1>
        <DataRefreshTimer :refetchLiveTrades="refetchLiveTrades" />
      </div>

      <!-- Portfolio Summary -->
      <PortfolioSummary />
    </header>

    <!-- Live Trades Grid -->
    <main v-if="activeTrades?.values" class="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
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
    </main>

    <!-- Empty State -->
    <div v-if="activeTrades?.length === 0" class="text-center py-12">
      <div class="text-6xl mb-4">📈</div>
      <h3 class="text-xl font-semibold text-gray-900 mb-2">No Active Trades</h3>
      <p class="text-gray-600">
        Your live trades will appear here once you convert trade ideas to positions.
      </p>
    </div>
  </main>
</template>
