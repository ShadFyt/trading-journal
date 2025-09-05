<script lang="ts" setup>
import { useLiveTradeFetchingService } from '@/composables'
import type { LiveTrade } from '@/interfaces'

const { watchlist } = useLiveTradeFetchingService()
const selectedTrade = ref<LiveTrade | null>(null)
</script>

<template>
  <aside class="w-100 h-screen bg-gray-900 border-r border-gray-800 flex flex-col">
    <div class="p-4 border-b border-gray-800">
      <h2 class="text-lg font-semibold text-white mb-3">Watchlist</h2>
      <div class="relative">
        <Input
          placeholder="Search symbols..."
          class="pl-10 bg-gray-800 border-gray-700 text-white placeholder-gray-400"
        />
      </div>
    </div>
    <div class="flex-1 flex flex-col min-h-0">
      <ScrollArea class="flex-1">
        <div class="p-2">
          <div
            v-for="trade in watchlist"
            :key="trade.id"
            :class="[
              'p-3 rounded-lg cursor-pointer transition-all hover:bg-gray-800 mb-1',
              selectedTrade?.id === trade.id ? 'bg-gray-800 ring-1 ring-blue-500' : '',
            ]"
          >
            <TradePriceDetail :trade />
          </div>
        </div>
      </ScrollArea>
    </div>
  </aside>
</template>
