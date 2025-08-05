<script setup lang="ts">
import { useLiveTradeFetchingService } from '@/composables/useLiveTradeService'
import LiveTrades from '@/components/live-trades/LiveTrades.vue'

const { liveTrades } = useLiveTradeFetchingService()
</script>
<template>
  <LiveTrades />
</template>
