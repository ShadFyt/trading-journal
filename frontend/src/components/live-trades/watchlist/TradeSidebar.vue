<script lang="ts" setup>
import { Icon } from '@iconify/vue'
import { useFormatters, useLiveTradeFetchingService } from '@/composables'
import type { LiveTrade } from '@/interfaces'

const { watchlist } = useLiveTradeFetchingService()
const { formatCurrency, formatPercentage } = useFormatters()
const selectedTrade = ref<LiveTrade | null>(null)

const getStatusColor = (status: string) => {
  switch (status) {
    case 'watching':
      return 'bg-blue-500/10 text-blue-400 border-blue-500/20'
    case 'alert':
      return 'bg-orange-500/10 text-orange-400 border-orange-500/20'
    default:
      return 'bg-gray-500/10 text-gray-400 border-gray-500/20'
  }
}
watch(
  () => watchlist,
  () => {
    console.log(watchlist.value)
  },
)
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
            <div class="flex items-center justify-between mb-1">
              <div class="flex items-center gap-2">
                <span class="font-semibold text-white text-sm">{{ trade.symbol }}</span>
                <Badge :class="[getStatusColor(trade.status), 'text-xs']">
                  {{ trade.status }}
                </Badge>
              </div>
              <Button variant="ghost" size="sm" class="h-6 w-6 p-0">
                <!--                <MoreVertical class="h-3 w-3 text-gray-400" />-->
              </Button>
            </div>

            <div class="flex justify-between items-center mb-1">
              <span class="text-white font-medium">{{ formatCurrency(trade.currentPrice) }}</span>
              <span
                v-if="trade.percentChange != null"
                class="text-xs"
                :class="trade.percentChange < 0 ? 'text-red-400' : 'text-green-400'"
                >{{ formatPercentage(trade.percentChange) }}</span
              >
            </div>

            <div class="flex justify-between text-xs text-gray-400">
              <!--              <span>Entry: {{ formatCurrency(trade.entry) }}</span>-->
              <span>Entry: 0</span>
              <div class="flex items-center gap-1">
                <Icon
                  v-for="i in trade.rating"
                  :key="i"
                  icon="lucide:star"
                  class="h-4 w-4 fill-yellow-400 text-yellow-400"
                />
              </div>
            </div>
          </div>
        </div>
      </ScrollArea>
    </div>
  </aside>
</template>
