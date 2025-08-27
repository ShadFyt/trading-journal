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
    <ScalePlanContentHeader :plan :id="trade.id" :idx />

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
