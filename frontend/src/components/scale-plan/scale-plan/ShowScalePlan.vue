<script setup lang="ts">
import { computed } from 'vue'
import type { ScalePlan } from '@/interfaces'
import { useFormatters } from '@/composables'
import { ScalePlanStatusEnum } from '@/enums'
const { formatCurrency } = useFormatters()

const { plan, idx } = defineProps<{
  plan: ScalePlan
  idx: number
}>()

const statusConfig = computed(() => {
  switch (plan.status) {
    case ScalePlanStatusEnum.enum.FILLED:
      return {
        badgeClass: 'bg-green-50 text-green-700 border-green-200',
        icon: '✓',
        label: 'filled',
      }
    case ScalePlanStatusEnum.enum.PARTIALLY_FILLED:
      return {
        badgeClass: 'bg-orange-50 text-orange-700 border-orange-200',
        icon: '~',
        label: 'partially filled',
      }
    case ScalePlanStatusEnum.enum.CANCELLED:
      return {
        badgeClass: 'bg-red-50 text-red-700 border-red-200',
        icon: '✕',
        label: 'cancelled',
      }
    case ScalePlanStatusEnum.enum.PLANNED:
    default:
      return {
        badgeClass: 'bg-gray-50 text-gray-700 border-gray-200',
        icon: '',
        label: 'planned',
      }
  }
})
</script>

<template>
  <HoverCardTrigger as-child>
    <Badge
      role="button"
      tabindex="0"
      class="text-xs focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
      :class="statusConfig.badgeClass"
      :aria-describedby="`sp-${plan.id}-title`"
    >
      T{{ idx + 1 }}: {{ formatCurrency(plan.targetPrice ?? 0) }}
      <span v-if="statusConfig.icon" class="ml-1">{{ statusConfig.icon }}</span>
      <span class="sr-only"> ({{ statusConfig.label }}) </span>
    </Badge>
  </HoverCardTrigger>
</template>
