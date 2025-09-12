<script lang="ts" setup>
import type { Trade, ScalePlan } from '@/interfaces'
import { useFormatters } from '@/composables'

const { plan } = defineProps<{
  trade: Trade
  plan: ScalePlan
  idx: number
}>()

const { formatTradeDate } = useFormatters()

const formatValue = (value?: number) => (typeof value === 'number' ? `${value} shares` : '—')

const pills = computed(() => [
  { label: 'Order', value: plan.orderType },
  { label: 'Quantity', value: formatValue(plan.qty) },
])
</script>

<template>
  <div>
    <ScalePlanContentHeader :plan :id="trade.id" :idx />

    <div class="my-2 border-t border-gray-200"></div>

    <ul class="flex flex-wrap gap-2 justify-around" role="list">
      <li v-for="p in pills" :key="p.label">
        <span class="text-xs rounded-full bg-slate-700 px-2 py-0.5"
          >{{ p.label }}: {{ p.value }}</span
        >
      </li>
    </ul>

    <ScalePlanTargetPanel :plan />

    <div v-if="plan.goodTillDate" class="text-xs text-gray-600">
      Good till: <span class="font-medium">{{ formatTradeDate(plan.goodTillDate) }}</span>
    </div>

    <div v-if="plan.notes" class="text-sm">
      <p class="text-xs text-gray-600 mb-1">Notes</p>
      <p class="leading-snug">{{ plan.notes }}</p>
    </div>
  </div>
</template>
