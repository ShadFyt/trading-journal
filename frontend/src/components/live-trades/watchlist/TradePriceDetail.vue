<script lang="ts" setup>
import { Icon } from '@iconify/vue'
import type { LiveTrade } from '@/interfaces'
import { useFormatters, useTradeMetrics } from '@/composables'
const { formatCurrency, formatPercentage } = useFormatters()

const { trade } = defineProps<{
  trade: LiveTrade
}>()

const { entryPrice } = useTradeMetrics(trade)

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
</script>

<template>
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
    <span>Entry: {{ formatCurrency(entryPrice) }}</span>
    <div class="flex items-center gap-1">
      <Icon
        v-for="i in trade.rating"
        :key="i"
        icon="lucide:star"
        class="h-4 w-4 fill-yellow-400 text-yellow-400"
      />
    </div>
  </div>
</template>
