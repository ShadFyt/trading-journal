<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'
import LiveTradeCard from './LiveTradeCard.vue'
import { useLiveTradeFetchingService } from '@/composables'
import PortfolioSummary from './PortfolioSummary.vue'
import { Icon } from '@iconify/vue'

const { liveTrades: activeTrades, refetchLiveTrades } = useLiveTradeFetchingService()

const refetchProgress = ref(0)

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

const handleRefresh = () => {
  refetchLiveTrades()
  refetchProgress.value = 0
}

let interval: ReturnType<typeof setInterval> | null = null

const startTimer = () => {
  refetchProgress.value = 0
  interval = setInterval(() => {
    refetchProgress.value += 1.6667 // 100% / 60 seconds ≈ 1.6667% per second
    if (refetchProgress.value >= 100) {
      handleRefresh()
      refetchProgress.value = 0 // Reset to 0 instead of clearing
    }
  }, 500) // Update every second for 60 seconds total
}

onMounted(() => {
  startTimer()
})

onUnmounted(() => {
  if (interval) {
    clearInterval(interval)
  }
})
</script>

<template>
  <main class="p-4 max-w-7xl mx-auto">
    <!-- Header -->
    <header class="mb-">
      <div class="flex justify-between items-center mb-2">
        <h1 class="text-3xl font-bold text-gray-900 mb-2">Live Trades</h1>
        <div class="w-1/3">
          <span class="text-sm text-gray-500">Data Refresh Timer</span>
          <div class="flex items-center gap-3">
            <Progress v-model="refetchProgress" class="w-5/5 h-3" />
            <Icon
              icon="lucide:refresh-cw"
              width="24"
              height="24"
              @click="handleRefresh"
              class="cursor-pointer hover:opacity-75"
            />
          </div>
        </div>
      </div>

      <!-- Portfolio Summary -->
      <PortfolioSummary />
    </header>

    <!-- Live Trades Grid -->
    <div v-if="activeTrades?.values" class="grid grid-cols-1 md:grid-cols-2 gap-6">
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
    <div v-if="activeTrades?.length === 0" class="text-center py-12">
      <div class="text-6xl mb-4">📈</div>
      <h3 class="text-xl font-semibold text-gray-900 mb-2">No Active Trades</h3>
      <p class="text-gray-600">
        Your live trades will appear here once you convert trade ideas to positions.
      </p>
    </div>
  </main>
</template>
