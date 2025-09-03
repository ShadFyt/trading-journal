<script setup lang="ts">
import type { LiveTrade } from '@/interfaces'
import { useFormatters, useTradeMetrics } from '@/composables'

const { trade } = defineProps<{ trade: LiveTrade }>()
const { remainingShares, entryPrice, initialPosition, stopLoss } = useTradeMetrics(trade)

const { formatCurrency } = useFormatters()
</script>

<template>
  <dl
    class="grid grid-cols-[max-content_1fr] md:grid-cols-[max-content_1fr_max-content_1fr] gap-x-4 gap-y-2 text-sm"
  >
    <KeyValueItem label="Entry:">
      {{ formatCurrency(entryPrice) }}
    </KeyValueItem>

    <KeyValueItem label="Stop Loss:">
      {{ formatCurrency(stopLoss) }}
    </KeyValueItem>

    <KeyValueItem label="Initial Position:"> {{ initialPosition }} shares </KeyValueItem>
    <KeyValueItem label="Remaining Position:"> {{ remainingShares }} shares </KeyValueItem>
    <KeyValueItem label="Rating:">
      <RatingBadge :rating="trade.rating" />
    </KeyValueItem>
  </dl>
</template>
