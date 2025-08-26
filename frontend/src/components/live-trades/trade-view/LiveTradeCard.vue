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

const ratingBadgeClass = computed(() => {
  const r = Math.max(0, Math.min(10, trade.rating ?? 0))
  if (r <= 2) return 'bg-red-100 text-red-800'
  if (r <= 4) return 'bg-orange-100 text-orange-800'
  if (r <= 6) return 'bg-yellow-100 text-yellow-800'
  if (r <= 8) return 'bg-green-100 text-green-800'
  return 'bg-emerald-100 text-emerald-800'
})
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
          <section class="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-2 text-sm mb-3">
            <div>
              <span class="font-semibold text-gray-600">Entry:</span>
              <span class="ml-1">{{ formatCurrency(trade.entryPriceAvg) }}</span>
            </div>
            <div>
              <span class="font-semibold text-gray-600">Stop Loss:</span>
              <span class="ml-1">{{ formatCurrency(trade.stop) }}</span>
            </div>
            <div>
              <span class="font-semibold text-gray-600">Position:</span>
              <span class="ml-1">{{ trade.positionSize }} shares</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="font-semibold text-gray-600">Rating:</span>
              <span
                class="inline-flex items-center rounded-full px-2 py-0.5 text-sm font-medium"
                :class="ratingBadgeClass"
                :aria-label="`Trade quality rating ${trade.rating}/10`"
              >
                {{ trade.rating }}/10
              </span>
            </div>
          </section>

          <ScalePlans :trade="trade" />

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
