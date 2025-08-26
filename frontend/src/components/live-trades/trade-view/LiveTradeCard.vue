<script setup lang="ts">
import { computed } from 'vue'
import { useToggle } from '@vueuse/core'

import { useFormatters } from '@/composables'
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

const { formatCurrency, formatTradeDuration } = useFormatters()

const [isExpanded, toggleExpanded] = useToggle(false)

const positionValue = computed(() => {
  const { positionSize, currentPrice } = trade
  return positionSize * currentPrice
})

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
          <div class="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-1 text-sm mb-3">
            <div>
              <span class="font-semibold text-gray-600">R:R Ratio:</span>
              <span class="ml-1">1:{{ trade.rrRatio?.toFixed(2) }}</span>
            </div>
            <div>
              <span class="font-semibold text-gray-600">Time in Trade:</span>
              <span class="ml-1">{{ formatTradeDuration(trade.enterDate) }}</span>
            </div>
            <div class="col-span-2">
              <span class="font-semibold text-gray-600">Position Value:</span>
              <span class="ml-1">{{ formatCurrency(positionValue) }}</span>
            </div>
          </div>

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
