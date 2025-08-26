<script setup lang="ts">
import type { LiveTrade } from '@/interfaces'
import { useFormatters } from '@/composables'

const { trade } = defineProps<{ trade: LiveTrade }>()
const { formatCurrency } = useFormatters()
</script>

<template>
  <dl
    class="grid grid-cols-[max-content_1fr] md:grid-cols-[max-content_1fr_max-content_1fr] gap-x-4 gap-y-2 text-sm"
  >
    <KeyValueItem label="Entry:">
      {{ formatCurrency(trade.entryPriceAvg) }}
    </KeyValueItem>

    <KeyValueItem label="Stop Loss:">
      {{ formatCurrency(trade.stop) }}
    </KeyValueItem>

    <KeyValueItem label="Position:"> {{ trade.positionSize }} shares </KeyValueItem>
    <KeyValueItem label="Rating:">
      <RatingBadge :rating="trade.rating" />
    </KeyValueItem>
  </dl>
</template>
