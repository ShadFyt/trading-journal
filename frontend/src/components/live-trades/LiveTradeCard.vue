<script setup lang="ts">
import { computed, ref } from 'vue'
import { ProgressIndicator, ProgressRoot } from 'reka-ui'

import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { useFormatters } from '@/composables'
import type { LiveTrade } from '@/interfaces/live-trade.type'

interface Props {
  trade: LiveTrade
}

const { trade } = defineProps<Props>()

/**
 * Emitted events for trade management actions
 */
const emit = defineEmits<{
  adjustStop: [tradeId: string, type: 'breakeven' | 'trailing']
  partialExit: [tradeId: string, percentage: number]
  addPosition: [tradeId: string]
  closeTrade: [tradeId: string]
  editTrade: [tradeId: string]
}>()

const { formatCurrency, formatPercentage, formatTradeDuration, convertStringToDate } =
  useFormatters()

/**
 * Status badge styling based on trade status
 */
const statusBadgeClass = computed(() => {
  const baseClasses =
    'cursor-pointer hover:opacity-80 capitalize px-3 py-1 text-xs rounded-full border font-semibold'

  switch (trade.status) {
    case 'open':
      return `${baseClasses} bg-blue-50 text-blue-700 border-blue-200`
    case 'partial':
      return `${baseClasses} bg-yellow-50 text-yellow-700 border-yellow-200`
    case 'closed':
      return `${baseClasses} bg-gray-50 text-gray-700 border-gray-200`
    default:
      return `${baseClasses} bg-gray-50 text-gray-700 border-gray-200`
  }
})

const targets = computed(() => trade.scalePlans.map(({ targetPrice }) => targetPrice))

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

/**
 * P&L styling based on profit/loss
 */
const pnlStyling = computed(() => {
  const isProfit = pnl.value >= 0
  return {
    textColor: isProfit ? 'text-green-600' : 'text-red-600',
    bgColor: isProfit ? 'bg-green-50' : 'bg-red-50',
    borderColor: isProfit ? 'border-green-200' : 'border-red-200',
  }
})

const isExpanded = ref(false)
</script>

<template>
  <Card
    class="relative transition-shadow hover:shadow-2xl border border-gray-200 rounded-xl bg-white shadow-sm overflow-hidden group animate-fadein"
  >
    <CardHeader>
      <DropdownMenu>
        <DropdownMenuTrigger class="absolute top-2 right-2">
          <Button
            variant="ghost"
            size="sm"
            aria-label="Open trade menu"
            aria-haspopup="menu"
            class="h-11 w-11 min-w-[44px] min-h-[44px] p-0 rounded-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2"
          >
            ⋯
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent side="bottom" align="end" :avoidCollisions="false">
          <DropdownMenuItem @click="emit('editTrade', trade.id)"> Edit Trade </DropdownMenuItem>
          <DropdownMenuItem @click="emit('adjustStop', trade.id, 'breakeven')">
            Move Stop to Breakeven
          </DropdownMenuItem>
          <DropdownMenuItem @click="emit('adjustStop', trade.id, 'trailing')">
            Set Trailing Stop
          </DropdownMenuItem>
          <DropdownMenuItem @click="emit('addPosition', trade.id)">
            Add to Position
          </DropdownMenuItem>
          <DropdownMenuItem class="text-red-600" @click="emit('closeTrade', trade.id)">
            Close Trade
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </CardHeader>

    <CardContent class="pt-0">
      <!-- Header Section -->
      <header class="flex justify-between items-center mb-3">
        <div class="flex items-center gap-2">
          <span class="text-base md:text-2xl">📈</span>
          <h2 class="text-lg md:text-2xl font-bold text-blue-700 tracking-wide">
            {{ trade.symbol.toUpperCase() }}
          </h2>
        </div>
        <Badge :class="statusBadgeClass">{{ trade.status }}</Badge>
      </header>

      <!-- P&L Display -->
      <div
        class="grid grid-cols-1 gap-2 md:grid-cols-3 md:items-center p-3 rounded-lg mb-3 border"
        :class="[pnlStyling.bgColor, pnlStyling.borderColor]"
      >
        <div>
          <p class="text-xs text-gray-600 uppercase tracking-wide">Current Price</p>
          <span
            class="text-lg md:text-xl font-bold"
            :class="trade.currentPrice >= trade.entryPriceAvg ? 'text-green-600' : 'text-red-600'"
            aria-live="polite"
            aria-atomic="true"
          >
            {{ formatCurrency(trade.currentPrice) }}
            <span class="sr-only">
              {{ trade.currentPrice >= trade.entryPriceAvg ? 'above entry' : 'below entry' }}
            </span>
          </span>
        </div>
        <div>
          <p class="text-xs text-gray-600 uppercase tracking-wide">Profit/Loss</p>
          <span
            class="text-xl md:text-2xl font-bold"
            :class="pnl >= 0 ? 'text-green-600' : 'text-red-600'"
            aria-live="polite"
            aria-atomic="true"
          >
            {{ (pnl >= 0 ? '+' : '') + formatCurrency(pnl) }}
          </span>
        </div>
        <div class="md:text-right">
          <p class="text-xs text-gray-600 uppercase tracking-wide">Percentage</p>
          <span
            class="text-sm"
            :class="pnl >= 0 ? 'text-green-600' : 'text-red-600'"
            aria-live="polite"
            aria-atomic="true"
            >{{
              formatPercentage(
                ((trade.currentPrice - trade.entryPriceAvg) / trade.entryPriceAvg) * 100,
              )
            }}</span
          >
        </div>
      </div>

      <transition name="fade">
        <div v-if="isExpanded" :id="'trade-details-' + trade.id">
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

          <div class="mb-3">
            <p class="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-1">Targets</p>
            <div class="flex flex-wrap gap-1">
              <Badge
                v-for="(target, idx) in targets"
                :key="idx"
                variant="outline"
                class="text-xs"
                :class="
                  trade.currentPrice >= (target ?? 0)
                    ? 'bg-green-50 text-green-700 border-green-200'
                    : 'bg-gray-50'
                "
              >
                T{{ idx + 1 }}: {{ formatCurrency(target ?? 0) }}
                <span v-if="trade.currentPrice >= (target ?? 0)" class="ml-1">✓</span>
                <span class="sr-only">
                  {{ trade.currentPrice >= (target ?? 0) ? '(reached)' : '(not reached)' }}
                </span>
              </Badge>
            </div>
          </div>

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
      </transition>

      <!-- Footer -->
      <footer
        class="mt-3 pt-2 border-t border-gray-100 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between flex-wrap text-xs text-gray-400"
      >
        <span>Entered {{ convertStringToDate(trade.enterDate).toLocaleDateString() }}</span>
        <button
          type="button"
          :aria-expanded="isExpanded"
          :aria-controls="'trade-details-' + trade.id"
          @click="isExpanded = !isExpanded"
          class="text-blue-600 inline-flex items-center h-11 px-3 min-w-[44px] rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2"
        >
          {{ isExpanded ? 'Collapse' : 'Expand' }}
        </button>
        <span>ID: {{ trade.id.slice(-6) }}</span>
      </footer>
    </CardContent>
  </Card>
</template>
