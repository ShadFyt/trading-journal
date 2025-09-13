<script lang="ts" setup>
import { ProgressIndicator, ProgressRoot } from 'reka-ui'
import { useFormatters } from '@/composables'

const { plannedShares, filledQty } = defineProps<{
  plannedShares: number
  filledQty: number
  commissions: number
}>()
const { formatCurrency } = useFormatters()

const fillPct = computed(() => {
  const planned = Number(plannedShares || 0)
  if (!Number.isFinite(planned) || planned <= 0) return 0
  const pct = (filledQty / planned) * 100
  return Math.max(0, Math.min(100, Math.round(pct)))
})

const ariaValueText = computed(
  () => `${filledQty} of ${plannedShares} shares filled (${fillPct.value}%)`,
)
</script>

<template>
  <div class="mb-2">
    <ProgressRoot
      :model-value="fillPct"
      class="rounded-full relative h-2 overflow-hidden bg-white dark:bg-stone-950 border border-muted motion-reduce:transition-none"
      role="progressbar"
      aria-label="Filled shares progress"
      :aria-valuemin="0"
      :aria-valuemax="100"
      :aria-valuenow="fillPct"
      :aria-valuetext="ariaValueText"
    >
      <ProgressIndicator
        class="indicator rounded-full block relative w-full h-full transition-transform overflow-hidden duration-[660ms] ease-[cubic-bezier(0.65, 0, 0.35, 1)] after:animate-progress after:content-[''] after:absolute after:inset-0 after:bg-[linear-gradient(-45deg,_rgba(255,255,255,0.2)_25%,_transparent_25%,_transparent_50%,_rgba(255,255,255,0.2)_50%,_rgba(255,255,255,0.2)_75%,_transparent_75%,_transparent)] after:bg-[length:30px_30px] motion-reduce:after:animate-none motion-reduce:transition-none bg-green-500"
        :style="`transform: translateX(-${100 - fillPct}%)`"
      />
    </ProgressRoot>
    <p class="mt-1 text-[11px] text-slate-300 text-center">
      {{ filledQty }} / {{ plannedShares }} shares ({{ fillPct }}%) • Commissions:
      {{ formatCurrency(commissions) }}
    </p>
  </div>
</template>
