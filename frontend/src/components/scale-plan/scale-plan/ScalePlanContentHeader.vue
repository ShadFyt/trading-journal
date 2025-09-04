<script lang="ts" setup>
import type { ScalePlan } from '@/interfaces'

const { plan } = defineProps<{ plan: ScalePlan; id: string; idx: number }>()

const statusBadgeClass = computed(() => {
  switch (plan.status) {
    case 'planned':
      return 'bg-blue-100 text-blue-800'
    case 'filled_partial':
      return 'bg-orange-100 text-orange-800'
    case 'filled':
      return 'bg-green-100 text-green-800'
    case 'cancelled':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-700'
  }
})
</script>

<template>
  <header class="flex items-center justify-between mb-1 pr-10">
    <h4 :id="`sp-${id}-title`" class="text-sm font-semibold text-blue-400">
      {{ plan.label?.trim() || `Plan ${idx + 1}` }}
    </h4>
    <Badge
      class="rounded-full px-2 py-0.5 text-[11px] font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
      :class="statusBadgeClass"
    >
      {{ plan.status }}
    </Badge>
  </header>
</template>
