<script setup lang="ts">
import { Icon } from '@iconify/vue'
import LiveTradeCard from './trade-view/LiveTradeCard.vue'
import { useLiveTradeFetchingService, useMediaQuery } from '@/composables'

import type { LiveTrade } from '@/interfaces/live-trade.type'
import { useToggle } from '@vueuse/core'

const { liveTrades: activeTrades, refetchLiveTrades } = useLiveTradeFetchingService()
const { isDesktop } = useMediaQuery()

const selectedTrade = ref<LiveTrade | null>(null)
const isEditFormOpen = ref(false)
const formType = ref<'edit' | 'close'>('edit')
const [isSidebarOpen, toggleSidebar] = useToggle(false)

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
  <div class="flex h-screen w-full bg-gray-950 relative">
    <Button
      v-if="!isDesktop"
      @click="() => toggleSidebar()"
      class="fixed top-4 right-4 z-50 bg-gray-800 hover:bg-gray-700 border-gray-600"
      size="sm"
      variant="outline"
    >
      <Icon icon="lucide:menu" class="h-4 w-4" />
    </Button>

    <main class="flex-1 p-4 overflow-auto">
      <PortfolioHeader @refetch-live-trades="refetchLiveTrades" />

      <!-- Live Trades Grid -->
      <section
        v-if="activeTrades?.length"
        class="grid grid-cols-1 md:grid-cols-2 gap-6 items-start"
      >
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
      <LiveTradeFormEdit
        v-if="selectedTrade"
        :trade="selectedTrade"
        :isOpen="isEditFormOpen"
        :close="handleFormClose"
        :formType="formType"
      />
    </main>

    <TradeSidebar :is-open="isSidebarOpen" />

    <div
      v-if="isSidebarOpen && !isDesktop"
      @click="() => toggleSidebar(false)"
      class="fixed inset-0 z-30 bg-black bg-opacity-50"
    />
  </div>
</template>
