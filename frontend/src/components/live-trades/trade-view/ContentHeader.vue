<script setup lang="ts">
import type { LiveTrade } from '@/interfaces'

const { trade } = defineProps<{ trade: LiveTrade }>()
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
</script>

<template>
  <header class="flex justify-between items-center mb-3">
    <div class="flex items-center gap-2">
      <span class="text-base md:text-2xl">📈</span>
      <h2 class="text-lg md:text-2xl font-bold text-blue-700 tracking-wide">
        {{ trade.symbol.toUpperCase() }}
      </h2>
    </div>
    <Badge :class="statusBadgeClass">{{ trade.status }}</Badge>
  </header>
</template>
