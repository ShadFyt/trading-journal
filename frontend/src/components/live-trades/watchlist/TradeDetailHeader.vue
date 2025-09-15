<script lang="ts" setup>
import type { Trade } from '@/interfaces'
const { trade } = defineProps<{ trade: Trade }>()
</script>

<template>
  <CardHeader class="flex items-center justify-between flex-shrink-0">
    <h3 class="text-white font-semibold text-sm">{{ trade?.symbol }} Details</h3>
    <div>
      <TradeActionMenu :trade="trade" />
    </div>
  </CardHeader>
</template>
