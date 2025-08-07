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

/**
 * Calculate progress percentage between stop loss and highest target
 */
const priceProgress = computed(() => {
  const { currentPrice, stop, targetPrices } = trade
  const highestTarget = Math.max(...targetPrices)
  const range = highestTarget - stop
  const progress = ((currentPrice - stop) / range) * 100
  return Math.max(0, Math.min(100, progress))
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
          <Button variant="ghost" size="sm">⋯</Button>
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
          <span class="text-2xl">📈</span>
          <h2 class="text-2xl font-bold text-blue-700 tracking-wide">
            {{ trade.symbol.toUpperCase() }}
          </h2>
        </div>
        <Badge :class="statusBadgeClass">{{ trade.status }}</Badge>
      </header>

      <!-- P&L Display -->
      <div
        class="flex justify-between items-center p-3 rounded-lg mb-3 border"
        :class="[pnlStyling.bgColor, pnlStyling.borderColor]"
      >
        <div>
          <p class="text-xs text-gray-600 uppercase tracking-wide">Current Price</p>
          <span
            class="text-xl font-bold"
            :class="trade.currentPrice >= trade.entryPriceAvg ? 'text-green-600' : 'text-red-600'"
            >{{ formatCurrency(trade.currentPrice) }}</span
          >
        </div>
        <div>
          <p class="text-xs text-gray-600 uppercase tracking-wide">Profit/Loss</p>
          <span class="text-2xl font-bold" :class="pnl >= 0 ? 'text-green-600' : 'text-red-600'">{{
            formatCurrency(pnl)
          }}</span>
        </div>
        <div class="text-right">
          <p class="text-xs text-gray-600 uppercase tracking-wide">Percentage</p>
          <span class="text-sm" :class="pnl >= 0 ? 'text-green-600' : 'text-red-600'">{{
            formatPercentage(
              ((trade.currentPrice - trade.entryPriceAvg) / trade.entryPriceAvg) * 100,
            )
          }}</span>
        </div>
      </div>

      <transition name="fade">
        <div v-if="isExpanded">
          <!-- Price Information -->
          <div class="grid grid-cols-2 gap-x-4 gap-y-2 text-sm mb-3">
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

          <!-- Target Prices -->
          <div class="mb-3">
            <p class="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-1">Targets</p>
            <div class="flex flex-wrap gap-1">
              <Badge
                v-for="(target, idx) in trade.targetPrices"
                :key="idx"
                variant="outline"
                class="text-xs"
                :class="
                  trade.currentPrice >= target
                    ? 'bg-green-50 text-green-700 border-green-200'
                    : 'bg-gray-50'
                "
              >
                T{{ idx + 1 }}: {{ formatCurrency(target) }}
                <span v-if="trade.currentPrice >= target" class="ml-1">✓</span>
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
              class="rounded-full relative h-3 overflow-hidden bg-white dark:bg-stone-950 border border-muted"
            >
              <ProgressIndicator
                class="indicator rounded-full block relative w-full h-full bg-grass9 transition-transform overflow-hidden duration-[660ms] ease-[cubic-bezier(0.65, 0, 0.35, 1)] after:animate-progress after:content-[''] after:absolute after:inset-0 after:bg-[linear-gradient(-45deg,_rgba(255,255,255,0.2)_25%,_transparent_25%,_transparent_50%,_rgba(255,255,255,0.2)_50%,_rgba(255,255,255,0.2)_75%,_transparent_75%,_transparent)] after:bg-[length:30px_30px]"
                :style="`transform: translateX(-${100 - priceProgress}%)`"
                :class="pnl >= 0 ? 'bg-green-500' : 'bg-red-500'"
              />
            </ProgressRoot>
          </div>

          <!-- Trade Metrics -->
          <div class="grid grid-cols-2 gap-x-4 gap-y-1 text-sm mb-3">
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
      <footer class="mt-3 pt-2 border-t border-gray-100 flex justify-between text-xs text-gray-400">
        <span>Entered {{ convertStringToDate(trade.enterDate).toLocaleDateString() }}</span>
        <button @click="isExpanded = !isExpanded" class="text-blue-500">
          {{ isExpanded ? 'Collapse' : 'Expand' }}
        </button>
        <span>ID: {{ trade.id.slice(-6) }}</span>
      </footer>
    </CardContent>
  </Card>
</template>
