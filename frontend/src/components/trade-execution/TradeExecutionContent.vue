<script lang="ts" setup>
import type { LiveTrade, ScalePlan } from '@/interfaces'
import { useFormatters } from '@/composables'
import { sharesFromPercent } from '@/utils'
const { convertStringToDate } = useFormatters()

const { plan, trade } = defineProps<{
  trade: LiveTrade
  plan: ScalePlan
  idx: number
}>()

const executions = computed(() => plan.executions)
const filledQty = computed(() => executions.value.reduce((total, exec) => total + exec.qty, 0))
const commissions = computed(() =>
  executions.value.reduce((total, exec) => total + exec.commission, 0),
)

const lastExecution = computed(() => executions.value[executions.value.length - 1])

const plannedShares = computed(() =>
  plan.kind === 'percent' ? sharesFromPercent(trade.positionSize, plan.value).shares : plan.value,
)
</script>

<template>
  <div>
    <ScalePlanContentHeader :plan :id="trade.id" :idx />

    <div class="my-2 border-t border-gray-200"></div>

    <PlanProgressBar :planned-shares="plannedShares" :filled-qty="filledQty" :commissions />

    <ExecutionSummary
      :executions
      :entry-price-avg="trade.entryPriceAvg"
      :target-price="plan.targetPrice"
      :stop="trade.stop"
    />

    <div v-if="lastExecution?.notes" class="text-sm">
      <p class="text-xs text-gray-600 mb-1">Notes</p>
      <p class="leading-snug">{{ lastExecution.notes }}</p>
    </div>
    <footer
      v-if="lastExecution"
      class="mt-3 pt-2 border-t border-gray-100 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between flex-wrap text-xs text-gray-400"
    >
      <span
        >Executed at: {{ convertStringToDate(lastExecution.executedAt).toLocaleDateString() }}</span
      >
    </footer>
  </div>
</template>
