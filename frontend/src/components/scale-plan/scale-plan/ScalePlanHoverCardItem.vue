<script setup lang="ts">
import { useFormatters } from '@/composables'
import type { LiveTrade, ScalePlan } from '@/interfaces'

const { formatTradeDate } = useFormatters()
const { plan, trade, idx } = defineProps<{
  trade: LiveTrade
  plan: ScalePlan
  idx: number
}>()

const emit = defineEmits<{
  (e: 'open-form', plan: ScalePlan, type: 'execute' | 'edit'): []
}>()

const formatValue = (kind: string, value?: number) =>
  typeof value === 'number' ? (kind === 'percent' ? `${value}%` : `${value} shares`) : '—'

// Local disclosure state
const hoverOpen = ref(false)
const menuOpen = ref(false)
const confirmOpen = ref(false)
const cardOpen = computed(() => hoverOpen.value || menuOpen.value || confirmOpen.value)

const onUpdateHover = (v: boolean) => {
  hoverOpen.value = v
}

const onOpenForm = (type: 'execute' | 'edit') => {
  emit('open-form', plan, type)
}

const pills = computed(() => [
  { label: 'Order', value: plan.orderType },
  { label: 'Kind', value: plan.kind },
  { label: 'Value', value: formatValue(plan.kind as string, plan.value) },
])
</script>

<template>
  <HoverCard :open="cardOpen" :open-delay="150" :close-delay="100" @update:open="onUpdateHover">
    <ScalePlanTrigger
      :targetPrice="plan.targetPrice"
      :executions="plan.executions"
      :positionSize="trade.positionSize"
      :id="plan.id"
      :idx="idx"
    />

    <HoverCardContent class="relative w-80 max-w-[90vw] p-2.5" align="start">
      <ScalePlanMenu
        :plan="plan"
        :idx="idx"
        v-model:menu-open="menuOpen"
        v-model:confirm-open="confirmOpen"
        @open-form="onOpenForm"
      />

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
    </HoverCardContent>
  </HoverCard>
</template>
