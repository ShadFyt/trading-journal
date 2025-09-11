<script setup lang="ts">
import PortfolioSummary from '@/components/live-trades/portfolio/PortfolioSummary.vue'
import type { RefetchOptions } from '@tanstack/vue-query'
const emit = defineEmits<{
  (e: 'refetch-live-trades', options?: RefetchOptions): void
}>()
</script>

<template>
  <header class="mb-">
    <div class="flex justify-between items-center mb-2">
      <h1 class="text-3xl font-bold text-blue-200">Live Trades</h1>
      <DataRefreshTimer @refetch-live-trades="emit('refetch-live-trades')" />
    </div>

    <!-- Portfolio Summary -->
    <PortfolioSummary />
  </header>
</template>
