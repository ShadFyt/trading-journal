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

const pills = computed(() => [
  { label: 'Order', value: plan.orderType },
  { label: 'Kind', value: plan.kind },
  { label: 'Value', value: formatValue(plan.kind as string, plan.value) },
])

const isFiniteNumber = (v: unknown): v is number => {
  return typeof v === 'number' && Number.isFinite(v)
}

const computeEffectiveShares = (
  baseShares: number,
  kind: string,
  value: unknown,
): number | null => {
  if (kind === 'shares') return isFiniteNumber(value) ? value : null
  if (kind === 'percent')
    return isFiniteNumber(value) ? Math.floor((baseShares * value) / 100) : null
  return null
}

const projectedPnLAtTarget = computed(() => {
  if (trade.entryPriceAvg == null || plan.targetPrice == null) return null

  const baseShares = trade.positionSize ?? 0
  const effectiveShares = computeEffectiveShares(baseShares, plan.kind as string, plan.value)
  if (!effectiveShares || effectiveShares <= 0) return null

  const isLong = true // TODO: infer from side/orderType
  const delta = isLong
    ? plan.targetPrice - trade.entryPriceAvg
    : trade.entryPriceAvg - plan.targetPrice
  return delta * effectiveShares
})

const projectedReturnPct = computed(() => {
  if (trade.entryPriceAvg == null || trade.entryPriceAvg === 0 || plan.targetPrice == null)
    return null
  const isLong = true

  const delta = isLong
    ? plan.targetPrice - trade.entryPriceAvg
    : trade.entryPriceAvg - plan.targetPrice
  return (delta / trade.entryPriceAvg) * 100
})

const pnlPercentBadgeClass = computed(() => {
  const v = Number(projectedReturnPct.value ?? NaN)
  if (!Number.isFinite(v)) return 'bg-gray-100 text-gray-800'
  if (v <= -5) return 'bg-red-100 text-red-800'
  if (v < -1) return 'bg-orange-100 text-orange-800'
  if (v < 1) return 'bg-gray-100 text-gray-800'
  if (v < 5) return 'bg-yellow-100 text-yellow-800'
  if (v < 10) return 'bg-green-100 text-green-800'
  return 'bg-emerald-100 text-emerald-800'
})
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

        <div class="grid grid-cols-2 gap-2 text-sm mt-2">
          <div v-if="plan.targetPrice != null" class="rounded bg-gray-50 p-2">
            <p class="text-xs text-gray-600">Target</p>
            <p class="font-medium">{{ formatCurrency(plan.targetPrice) }}</p>
          </div>

          <div v-if="projectedPnLAtTarget != null" class="rounded bg-gray-50 p-2">
            <p class="text-xs text-gray-600">Projected P&amp;L (target)</p>
            <p class="font-medium">
              {{ formatCurrency(projectedPnLAtTarget) }}
              <span
                v-if="projectedReturnPct != null"
                class="text-xs text-gray-600 rounded-full px-2 py-0.5"
                :class="pnlPercentBadgeClass"
                :aria-label="`Projected return ${projectedReturnPct.toFixed(2)}% at target`"
              >
                ({{ projectedReturnPct.toFixed(2) }}%)
              </span>
            </p>
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
