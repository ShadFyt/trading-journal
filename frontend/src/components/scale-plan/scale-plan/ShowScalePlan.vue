<script setup lang="ts">
import { computed } from 'vue'
import type { ExecutionDto } from '@/interfaces'
import { useFormatters } from '@/composables'
const { formatCurrency } = useFormatters()

const { targetPrice, executions, positionSize } = defineProps<{
  targetPrice: number | undefined
  executions: ExecutionDto[]
  positionSize: number
  id: string
  idx: number
}>()

const isReached = computed(() => {
  const qty = executions.reduce((total, exec) => total + exec.qty, 0)
  return qty === positionSize
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
      :aria-describedby="`sp-${id}-title`"
    >
      T{{ idx + 1 }}: {{ formatCurrency(targetPrice ?? 0) }}
      <span v-if="isReached" class="ml-1">✓</span>
      <span class="sr-only">
        {{ isReached ? '(reached)' : '(not reached)' }}
      </span>
    </Badge>
  </HoverCardTrigger>
</template>
