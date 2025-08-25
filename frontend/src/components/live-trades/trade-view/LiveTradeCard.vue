<script setup lang="ts">
import { computed, ref } from 'vue'
import { ProgressIndicator, ProgressRoot } from 'reka-ui'
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

/**
 * Calculate progress percentage between stop loss and highest target
 */
const priceProgress = computed(() => {
  const highest = trade.scalePlans.reduce<number | null>((max, { targetPrice }) => {
    return typeof targetPrice === 'number' && Number.isFinite(targetPrice)
      ? max === null
        ? targetPrice
        : Math.max(max, targetPrice)
      : max
  }, null)

  if (highest == null) return 100
  const range = highest - trade.stop
  if (range <= 0) return 100

  const clamp = (v: number, min = 0, max = 100) => Math.max(min, Math.min(max, v))
  return clamp(((trade.currentPrice - trade.stop) / range) * 100)
})

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
          <div class="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-2 text-sm mb-3">
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
          </div>

          <ScalePlans :trade="trade" />

          <!-- Price Progress Bar -->
          <div class="mb-3">
            <div class="flex justify-between text-xs text-gray-600 mb-1">
              <span>Stop</span>
              <span>Current Position</span>
              <span>Target</span>
            </div>
            <ProgressRoot
              v-model="priceProgress"
              class="rounded-full relative h-3 overflow-hidden bg-white dark:bg-stone-950 border border-muted motion-reduce:transition-none"
              role="progressbar"
              aria-label="Price progress toward target"
              :aria-valuemin="0"
              :aria-valuemax="100"
              :aria-valuenow="Math.round(priceProgress)"
            >
              <ProgressIndicator
                class="indicator rounded-full block relative w-full h-full bg-grass9 transition-transform overflow-hidden duration-[660ms] ease-[cubic-bezier(0.65, 0, 0.35, 1)] after:animate-progress after:content-[''] after:absolute after:inset-0 after:bg-[linear-gradient(-45deg,_rgba(255,255,255,0.2)_25%,_transparent_25%,_transparent_50%,_rgba(255,255,255,0.2)_50%,_rgba(255,255,255,0.2)_75%,_transparent_75%,_transparent)] after:bg-[length:30px_30px] motion-reduce:after:animate-none motion-reduce:transition-none"
                :style="`transform: translateX(-${100 - priceProgress}%)`"
                :class="pnl >= 0 ? 'bg-green-500' : 'bg-red-500'"
              />
            </ProgressRoot>
          </div>

          <!-- Trade Metrics -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-x-4 gap-y-1 text-sm mb-3">
            <div>
              <span class="font-semibold text-gray-600">R:R Ratio:</span>
              <span class="ml-1">1:{{ trade.rrRatio }}</span>
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
