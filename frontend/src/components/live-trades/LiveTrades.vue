<script setup lang="ts">
import LiveTradeCard from './trade-view/LiveTradeCard.vue'
import { useLiveTradeFetchingService } from '@/composables'

import type { LiveTrade } from '@/interfaces/live-trade.type'

const { liveTrades: activeTrades, refetchLiveTrades } = useLiveTradeFetchingService()

const selectedTrade = ref<LiveTrade | null>(null)
const isEditFormOpen = ref(false)
const formType = ref<'edit' | 'close'>('edit')

/**
 * Handle trade management actions
 */

const handleFormClose = () => {
  isEditFormOpen.value = false
  selectedTrade.value = null
}

const handleEditTrade = (tradeId: string, isClose: boolean = false) => {
  console.log(`Editing trade ${tradeId}`)
  if (!activeTrades.value) return
  selectedTrade.value = activeTrades.value?.find((trade) => trade.id === tradeId) ?? null
  isEditFormOpen.value = true
  formType.value = isClose ? 'close' : 'edit'
}

const handleCloseTrade = (tradeId: string) => {
  console.log(`Closing trade ${tradeId}`)
  handleEditTrade(tradeId, true)
}

// Split trades into two columns (stable stacks)
const leftTrades = computed(() => activeTrades.value?.filter((_, i) => i % 2 === 0) ?? [])
const rightTrades = computed(() => activeTrades.value?.filter((_, i) => i % 2 === 1) ?? [])
</script>

<template>
  <main class="p-4 max-w-7xl mx-auto">
    <PortfolioHeader @refetch-live-trades="refetchLiveTrades" />

    <!-- Live Trades Grid -->
    <section v-if="activeTrades?.length" class="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
      <div class="flex flex-col gap-6">
        <LiveTradeCard
          v-for="trade in leftTrades"
          :key="trade.id"
          :trade
          @close-trade="handleCloseTrade"
          @edit-trade="handleEditTrade"
        />
      </div>
      <div class="flex flex-col gap-6">
        <LiveTradeCard
          v-for="trade in rightTrades"
          :key="trade.id"
          :trade
          @close-trade="handleCloseTrade"
          @edit-trade="handleEditTrade"
        />
      </div>
    </section>

    <!-- Empty State -->
    <div v-if="!activeTrades?.length" class="text-center py-12">
      <div class="text-6xl mb-4">📈</div>
      <h3 class="text-xl font-semibold text-gray-900 mb-2">No Active Trades</h3>
      <p class="text-gray-600">
        Your live trades will appear here once you convert trade ideas to positions.
      </p>
    </div>
  </main>
  <LiveTradeFormEdit
    v-if="selectedTrade"
    :trade="selectedTrade"
    :isOpen="isEditFormOpen"
    :close="handleFormClose"
    :formType="formType"
  />
</template>
