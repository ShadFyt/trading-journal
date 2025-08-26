<script setup lang="ts">
import { computed } from 'vue'
import { useToggle } from '@vueuse/core'

import type { LiveTrade } from '@/interfaces/live-trade.type.ts'

interface Props {
  trade: LiveTrade
}

const { trade } = defineProps<Props>()

/**
 * Emitted events for trade management actions
 */
const emit = defineEmits<{
  'close-trade': [tradeId: string]
  'edit-trade': [tradeId: string]
}>()

const [isExpanded, toggleExpanded] = useToggle(false)

/**
 * Calculate P&L based on current price vs entry price
 */
const pnl = computed(() => {
  return (trade.currentPrice - trade.entryPriceAvg) * trade.positionSize
})

const detailsId = computed(() => `trade-details-${trade.id}`)
</script>

<template>
  <Card
    class="relative transition-shadow hover:shadow-2xl border border-gray-200 rounded-xl bg-white shadow-sm overflow-hidden group animate-fadein"
  >
    <CardHeader>
      <MenuHeader
        :trade="trade"
        @close-trade="emit('close-trade', trade.id)"
        @edit-trade="emit('edit-trade', trade.id)"
      />
    </CardHeader>

    <CardContent class="pt-0">
      <ContentHeader :trade />

      <ProfitLossDisplay :trade :pnl />

      <Transition name="fade">
        <div v-if="isExpanded" :id="detailsId">
          <!-- Price Information -->
          <PriceInfo :trade />

          <ScalePlans :trade />

          <!-- Price Progress Bar -->
          <TradeProgressBar :pnl :trade />

          <!-- Trade Metrics -->
          <TradeMetrics :trade />

          <!-- Setup & Notes -->
          <NotesDisplay :trade="trade" />
        </div>
      </Transition>

      <!-- Footer -->
      <TradeFooter
        :trade
        :is-expanded="isExpanded"
        :details-id="detailsId"
        @toggle="toggleExpanded()"
      />
    </CardContent>
  </Card>
</template>
