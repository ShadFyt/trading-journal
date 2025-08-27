<script lang="ts" setup>
import type { LiveTrade, ScalePlan } from '@/interfaces'
import { useFormatters } from '@/composables'

const { plan } = defineProps<{
  trade: LiveTrade
  plan: ScalePlan
  idx: number
}>()

const { formatTradeDate } = useFormatters()

const formatValue = (kind: string, value?: number) =>
  typeof value === 'number' ? (kind === 'percent' ? `${value}%` : `${value} shares`) : '—'

const pills = computed(() => [
  { label: 'Order', value: plan.orderType },
  { label: 'Kind', value: plan.kind },
  { label: 'Value', value: formatValue(plan.kind as string, plan.value) },
])
</script>

<template>
  <div>
    <div class="flex items-center justify-between mb-1 pr-10">
      <h4 :id="`sp-${trade.id}-title`" class="text-sm font-semibold">
        {{ plan.label?.trim() || `Plan ${idx + 1}` }}
      </h4>
      <Badge
        class="rounded-full bg-gray-100 text-gray-700 px-2 py-0.5 text-[11px] font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
      >
        {{ plan.status }}
      </Badge>
    </div>

    <div class="my-2 border-t border-gray-200"></div>

    <ul class="flex flex-wrap gap-2 justify-around" role="list">
      <li v-for="p in pills" :key="p.label">
        <span class="text-xs rounded-full bg-gray-100 px-2 py-0.5"
          >{{ p.label }}: {{ p.value }}</span
        >
      </li>
    </ul>

    <ScalePlanTargetPanel :trade :plan />

    <div v-if="plan.goodTillDate" class="text-xs text-gray-600">
      Good till: <span class="font-medium">{{ formatTradeDate(plan.goodTillDate) }}</span>
    </div>

    <div v-if="plan.notes" class="text-sm">
      <p class="text-xs text-gray-600 mb-1">Notes</p>
      <p class="leading-snug">{{ plan.notes }}</p>
    </div>
  </div>
</template>
