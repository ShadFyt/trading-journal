<script lang="ts" setup>
import type { Trade } from '@/interfaces'
import { useFormatters, useTradeMetrics } from '@/composables'

const { formatCurrency } = useFormatters()
const { selectedTrade } = defineProps<{ selectedTrade: Trade }>()
const emit = defineEmits<{
  'open-execution-form': []
  'open-trade-form': []
}>()
const { entryPrice, stopLoss } = useTradeMetrics(selectedTrade)
</script>

<template>
  <div class="h-full flex flex-col">
    <Card class="p-3 m-2 bg-gray-800/50 border-none flex flex-col flex-1 min-h-0">
      <CardHeader class="flex items-center justify-between flex-shrink-0">
        <h3 class="text-white font-semibold text-sm">{{ selectedTrade?.symbol }} Details</h3>
        <div class="flex gap-2">
          <Button
            @click="emit('open-execution-form')"
            size="sm"
            class="h-7 px-3 text-xs bg-blue-600 hover:bg-blue-700"
          >
            Trade
          </Button>
          <Button
            @click="emit('open-trade-form')"
            size="sm"
            class="h-7 px-3 text-xs bg-blue-600 hover:bg-blue-700"
          >
            Edit
          </Button>
        </div>
      </CardHeader>
      <div class="flex-1 overflow-y-auto">
        <CardContent class="pb-4">
          <div class="grid grid-cols-2 gap-x-4 gap-y-3 mb-4">
            <div>
              <p class="text-gray-400 text-xs mb-1">Last Price</p>
              <p class="text-white font-medium">{{ formatCurrency(selectedTrade.currentPrice) }}</p>
            </div>
            <div>
              <p class="text-gray-400 text-xs mb-1">Entry Target</p>
              <p class="text-blue-400 font-medium">{{ formatCurrency(entryPrice) }}</p>
            </div>
            <div>
              <p class="text-gray-400 text-xs mb-1">Stop Loss</p>
              <p class="text-red-400 font-medium">{{ formatCurrency(stopLoss) }}</p>
            </div>
            <div>
              <p class="text-gray-400 text-xs mb-1">Target 1</p>
              <p class="text-green-400 font-medium">$50.50</p>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-x-4 gap-y-3 mb-4">
            <div>
              <p class="text-gray-400 text-xs mb-1">R/R Ratio</p>
              <p class="text-white font-medium">{{ selectedTrade.rrRatio }}</p>
            </div>
            <div>
              <p class="text-gray-400 text-xs mb-1">Timeframe</p>
              <p class="text-white font-medium">3-6 months</p>
            </div>
          </div>

          <div>
            <p class="text-gray-400 text-xs mb-2">Notes</p>
            <p class="text-gray-300 text-xs leading-relaxed">
              Strong dividend yield, pipeline expansion projects looking promising. Good entry point
              after recent pullback.
            </p>
          </div>

          <!--    fetch sector and cap from finnhub api  -->
          <div class="mt-4 pt-3 border-t border-gray-700">
            <div class="flex items-center justify-between">
              <span class="text-blue-400 text-xs font-medium">Energy</span>
              <span class="text-gray-400 text-xs">Cap: 98.2B</span>
            </div>
          </div>
        </CardContent>
      </div>
    </Card>
  </div>
</template>
