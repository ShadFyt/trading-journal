<script setup lang="ts">
import { useFormatters } from '@/composables'
import type { LiveTrade, ScalePlan } from '@/interfaces'

const { formatCurrency, formatTradeDate } = useFormatters()
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
        <div class="flex items-center justify-between mb-1 pr-12">
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

        <div class="flex flex-wrap gap-1.5 text-[11px] mb-3">
          <span class="rounded-full bg-gray-100 px-2 py-0.5">Order: {{ plan.orderType }}</span>
          <span class="rounded-full bg-gray-100 px-2 py-0.5">Kind: {{ plan.kind }}</span>
          <span class="rounded-full bg-gray-100 px-2 py-0.5">
            Value: {{ formatValue(plan.kind as string, plan.value) }}
          </span>
        </div>

        <div class="grid grid-cols-2 gap-2 text-sm mt-2">
          <div v-if="plan.entryPrice != null" class="rounded bg-gray-50 p-2">
            <p class="text-xs text-gray-600">Entry</p>
            <p class="font-medium">{{ formatCurrency(plan.entryPrice) }}</p>
          </div>
          <div v-if="plan.targetPrice != null" class="rounded bg-gray-50 p-2">
            <p class="text-xs text-gray-600">Target</p>
            <p class="font-medium">{{ formatCurrency(plan.targetPrice) }}</p>
          </div>
          <div v-if="plan.stopPrice != null" class="rounded bg-gray-50 p-2">
            <p class="text-xs text-gray-600">Stop</p>
            <p class="font-medium">{{ formatCurrency(plan.stopPrice) }}</p>
          </div>
          <div v-if="plan.limitPrice != null" class="rounded bg-gray-50 p-2">
            <p class="text-xs text-gray-600">Limit</p>
            <p class="font-medium">{{ formatCurrency(plan.limitPrice) }}</p>
          </div>
        </div>

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
