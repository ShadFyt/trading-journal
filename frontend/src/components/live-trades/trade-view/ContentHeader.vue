<script setup lang="ts">
import { Icon } from '@iconify/vue'
import type { Trade } from '@/interfaces'
import { useTradeMetrics } from '@/composables'
import { ScaleTradeTypeEnum } from '@/enums'

const { trade } = defineProps<{ trade: Trade }>()
const tradeMetrics = useTradeMetrics(trade)

const isLong = computed(
  () => tradeMetrics.entryPlan.value.tradeType === ScaleTradeTypeEnum.enum.LONG,
)

const statusBadgeClass = computed(() => {
  const baseClasses =
    'cursor-pointer hover:opacity-80 capitalize px-3 py-1 text-xs rounded-full border font-semibold'

  switch (trade.status) {
    case 'open':
      return `${baseClasses} bg-blue-50 text-blue-700 border-blue-200`
    case 'watching':
      return `${baseClasses} bg-yellow-50 text-yellow-700 border-yellow-200`
    case 'closed':
      return `${baseClasses} bg-gray-50 text-gray-700 border-gray-200`
    default:
      return `${baseClasses} bg-gray-50 text-gray-700 border-gray-200`
  }
})

const tradeTypeBadgeClass = computed(() => {
  const baseClasses = 'px-2 py-1 text-xs rounded-full font-semibold uppercase tracking-wide'

  return isLong
    ? `${baseClasses} bg-green-100 text-green-700 border border-green-200`
    : `${baseClasses} bg-red-100 text-red-700 border border-red-200`
})
</script>

<template>
  <header class="flex justify-between items-center mb-3">
    <div class="flex items-center gap-2">
      <span class="text-base md:text-2xl">
        <Icon
          :icon="isLong ? 'lucide:trending-up' : 'lucide:trending-down'"
          :class="isLong ? 'text-green-400' : 'text-red-400'"
        />
      </span>
      <h2 class="text-lg md:text-2xl font-bold text-blue-400 tracking-wide">
        {{ trade.symbol.toUpperCase() }}
      </h2>
      <Badge :class="tradeTypeBadgeClass">
        {{ tradeMetrics.entryPlan.value.tradeType }}
      </Badge>
    </div>
    <Badge :class="statusBadgeClass">{{ trade.status }}</Badge>
  </header>
</template>
