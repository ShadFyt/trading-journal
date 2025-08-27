<script setup lang="ts">
import { computed } from 'vue'
import type { ScalePlan } from '@/interfaces'
import { useFormatters } from '@/composables'
import { sharesFromPercent } from '@/utils'
const { formatCurrency } = useFormatters()

const { plan, positionSize } = defineProps<{
  plan: ScalePlan
  positionSize: number
  idx: number
}>()

const isReached = computed(() => {
  const shares =
    plan.kind === 'percent' ? sharesFromPercent(positionSize, plan.value).shares : plan.value
  const qty = plan.executions.reduce((total, exec) => total + exec.qty, 0)
  return qty === shares
})

const badgeClass = computed(() => {
  return isReached.value
    ? 'bg-green-50 text-green-700 border-green-200'
    : 'bg-gray-50 text-gray-700 border-gray-200'
})
</script>

<template>
  <HoverCardTrigger as-child>
    <Badge
      role="button"
      tabindex="0"
      class="text-xs focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
      :class="badgeClass"
      :aria-describedby="`sp-${plan.id}-title`"
    >
      T{{ idx + 1 }}: {{ formatCurrency(plan.targetPrice ?? 0) }}
      <span v-if="isReached" class="ml-1">✓</span>
      <span class="sr-only">
        {{ isReached ? '(reached)' : '(not reached)' }}
      </span>
    </Badge>
  </HoverCardTrigger>
</template>
