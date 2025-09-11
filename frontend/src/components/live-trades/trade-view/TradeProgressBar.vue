<script lang="ts" setup>
import { ProgressIndicator, ProgressRoot } from 'reka-ui'
import { useInjectTradeMetrics } from '@/composables'

const { totalPnL, stopLoss, trade } = useInjectTradeMetrics()

/**
 * Calculate progress percentage between stop loss and highest target
 */
const priceProgress = computed(() => {
  const highest = trade.scalePlans.reduce<number | null>((max, { targetPrice }) => {
    return typeof targetPrice === 'number' && Number.isFinite(targetPrice)
      ? max === null
        ? targetPrice
        : Math.max(max, targetPrice)
      : max
  }, null)

  if (highest == null) return 100
  const range = highest - stopLoss
  if (range <= 0) return 100

  const clamp = (v: number, min = 0, max = 100) => Math.max(min, Math.min(max, v))
  return clamp(((trade.currentPrice - stopLoss) / range) * 100)
})

const ariaValueText = computed(() => `${Math.round(priceProgress.value)} percent toward target`)
</script>

<template>
  <div class="mb-3">
    <div class="flex justify-between text-xs text-gray-300 mb-1">
      <slot name="labels">
        <span>Stop</span>
        <span>Current Position</span>
        <span>Target</span>
      </slot>
    </div>
    <ProgressRoot
      :model-value="priceProgress"
      class="rounded-full relative h-3 overflow-hidden bg-white dark:bg-stone-950 border border-muted motion-reduce:transition-none"
      role="progressbar"
      aria-label="Price progress toward target"
      :aria-valuemin="0"
      :aria-valuemax="100"
      :aria-valuenow="Math.round(priceProgress)"
      :aria-valuetext="ariaValueText"
    >
      <ProgressIndicator
        class="indicator rounded-full block relative w-full h-full bg-grass9 transition-transform overflow-hidden duration-[660ms] ease-[cubic-bezier(0.65, 0, 0.35, 1)] after:animate-progress after:content-[''] after:absolute after:inset-0 after:bg-[linear-gradient(-45deg,_rgba(255,255,255,0.2)_25%,_transparent_25%,_transparent_50%,_rgba(255,255,255,0.2)_50%,_rgba(255,255,255,0.2)_75%,_transparent_75%,_transparent)] after:bg-[length:30px_30px] motion-reduce:after:animate-none motion-reduce:transition-none"
        :style="`transform: translateX(-${100 - priceProgress}%)`"
        :class="totalPnL >= 0 ? 'bg-green-500' : 'bg-red-500'"
      />
    </ProgressRoot>
  </div>
</template>
