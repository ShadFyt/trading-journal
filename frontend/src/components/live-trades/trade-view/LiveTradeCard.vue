<script setup lang="ts">
import { computed } from 'vue'
import { useToggle } from '@vueuse/core'

import type { LiveTrade } from '@/interfaces/live-trade.type.ts'
import { TRADE_METRICS_KEY, useTradeMetrics } from '@/composables'

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
const tradeMetrics = useTradeMetrics(trade)

const [isExpanded, toggleExpanded] = useToggle(false)

const detailsId = computed(() => `trade-details-${trade.id}`)
const pnlStyling = computed(() => {
  const isProfit = tradeMetrics.realizedPnL.value > 0
  if (tradeMetrics.totalPnL.value < 0) return 'border-red-200'
  if (isProfit) return 'border-green-200'
  return 'border-grey-200'
})

provide(TRADE_METRICS_KEY, tradeMetrics)
</script>

<template>
  <Card
    class="relative transition-shadow hover:shadow-2xl border bg-white shadow-sm overflow-hidden group animate-fadein"
    :class="pnlStyling"
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

      <ProfitLossDisplay />
      <ScalePlans :trade />

      <Transition name="fade">
        <div v-if="isExpanded" :id="detailsId">
          <!-- Price Information -->
          <PriceInfo />

          <!-- Price Progress Bar -->
          <TradeProgressBar />

          <!-- Trade Metrics -->
          <TradeMetrics />

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
