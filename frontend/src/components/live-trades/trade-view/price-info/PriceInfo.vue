<script setup lang="ts">
import { useFormatters, useInjectTradeMetrics } from '@/composables'

const {
  remainingShares,
  entryPrice,
  initialPosition,
  stopLoss,
  trade: { rating },
} = useInjectTradeMetrics()

const { formatCurrency } = useFormatters()
</script>

<template>
  <dl
    class="grid grid-cols-[max-content_1fr] md:grid-cols-[max-content_1fr_max-content_1fr] gap-x-4 gap-y-2 text-sm mb-2"
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
      <RatingBadge :rating />
    </KeyValueItem>
  </dl>
</template>
