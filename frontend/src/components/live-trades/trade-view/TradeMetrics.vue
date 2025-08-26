<script lang="ts" setup>
import type { LiveTrade } from '@/interfaces'
import { useFormatters } from '@/composables'
const { trade } = defineProps<{ trade: LiveTrade }>()
const { formatCurrency, formatTradeDuration } = useFormatters()

const positionValue = computed(() => {
  const { positionSize, currentPrice } = trade
  return positionSize * currentPrice
})
</script>

<template>
  <dl
    class="grid grid-cols-[max-content_1fr] md:grid-cols-[max-content_1fr_max-content_1fr] gap-x-4 gap-y-2 text-sm"
  >
    <KeyValueItem label="R:R Ratio:"> 1:{{ trade.rrRatio?.toFixed(2) }} </KeyValueItem>
    <KeyValueItem label="Time in Trade:">
      {{ formatTradeDuration(trade.enterDate) }}
    </KeyValueItem>
    <KeyValueItem label="Position Value:">
      {{ formatCurrency(positionValue) }}
    </KeyValueItem>
  </dl>
</template>
