<script lang="ts" setup>
import { Popover, PopoverAnchor, PopoverContent } from '@/components/ui/popover'
import type { LiveTrade, ScalePlan } from '@/interfaces'
import { ref } from 'vue'
import ScalePlanHoverCard from '@/components/scale-plan/scale-plan/ScalePlanHoverCard.vue'
import { useSorted } from '@vueuse/core'
import { ScalePlanStatusEnum } from '@/enums'

const { trade } = defineProps<{
  trade: LiveTrade
}>()

const selectedPlan = ref<null | ScalePlan>(null)
const isFormOpen = ref(false)
const formType = ref<'edit' | 'execute' | null>(null)

const plans = useSorted(
  () => trade.scalePlans.filter((plan) => plan.status !== ScalePlanStatusEnum.enum.CANCELLED) ?? [],
  (a, b) => {
    const at = a.targetPrice ?? Infinity
    const bt = b.targetPrice ?? Infinity
    return at - bt
  },
)

const openForm = (scalePlan: ScalePlan, type: 'edit' | 'execute') => {
  selectedPlan.value = scalePlan
  isFormOpen.value = true
  formType.value = type
}

const closeEditForm = () => {
  selectedPlan.value = null
  isFormOpen.value = false
}
</script>

<template>
  <Popover v-model:open="isFormOpen">
    <PopoverAnchor as-child>
      <div class="mb-3">
        <div class="flex justify-between">
          <p class="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-1">Targets</p>
          <ScalePlanQuickAdd :trade="trade" />
        </div>
        <div class="flex flex-wrap gap-1">
          <ScalePlanHoverCard
            v-for="(plan, idx) in plans"
            :key="plan.id"
            @open-form="openForm"
            :trade="trade"
            :plan="plan"
            :idx="idx"
          />
        </div>
      </div>
    </PopoverAnchor>
    <PopoverContent side="bottom" align="start">
      <ScalePlanQuickEdit
        v-if="selectedPlan && formType === 'edit'"
        :scalePlan="selectedPlan"
        :trade="trade"
        @close="closeEditForm"
      />
      <TradeExecutionForm
        v-if="selectedPlan && formType === 'execute'"
        :scalePlan="selectedPlan"
        @close="closeEditForm"
      />
    </PopoverContent>
  </Popover>
</template>
