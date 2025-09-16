<script lang="ts" setup>
import type { Trade } from '@/interfaces'

const { trade } = defineProps<{ trade: Trade }>()
</script>

<template>
  <CardHeader class="flex items-center justify-between flex-shrink-0">
    <div class="flex items-center gap-2">
      <CompanyLogo :trade />
      <h3 class="text-white font-semibold text-sm">{{ trade.name ?? trade.symbol }}</h3>
    </div>
    <div>
      <TradeActionMenu :trade="trade" />
    </div>
  </CardHeader>
</template>
