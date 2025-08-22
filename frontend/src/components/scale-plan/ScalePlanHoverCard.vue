<script setup lang="ts">
import type { LiveTrade } from '@/interfaces'
import ScalePlanHoverCardItem from '@/components/scale-plan/ScalePlanHoverCardItem.vue'
import { useSorted } from '@vueuse/core'

const { trade } = defineProps<{
  trade: LiveTrade
}>()

const plans = useSorted(
  () => trade.scalePlans ?? [],
  (a, b) => {
    const at = a.targetPrice ?? Infinity
    const bt = b.targetPrice ?? Infinity
    return at - bt
  },
)
</script>

<template>
  <div class="flex flex-wrap gap-1">
    <ScalePlanHoverCardItem
      v-for="(plan, idx) in plans"
      :key="plan.id ?? idx"
      :trade="trade"
      :plan="plan"
      :idx="idx"
      @openForm="$emit('open-form', plan, 'edit')"
    />
  </div>
</template>
