<script setup lang="ts">
import type { LiveTrade } from '@/interfaces'
import { computed } from 'vue'
import ScalePlanHoverCardItem from '@/components/scale-plan/ScalePlanHoverCardItem.vue'

const { trade } = defineProps<{
  trade: LiveTrade
}>()

const plans = computed(() => trade.scalePlans ?? [])
</script>

<template>
  <div class="flex flex-wrap gap-1">
    <ScalePlanHoverCardItem
      v-for="(plan, idx) in plans"
      :key="plan.id ?? idx"
      :trade="trade"
      :plan="plan"
      :idx="idx"
      @edit="$emit('edit', plan)"
    />
  </div>
</template>
