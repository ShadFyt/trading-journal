<script lang="ts" setup>
import { Popover, PopoverAnchor, PopoverContent } from '@/components/ui/popover'
import type { LiveTrade, ScalePlan } from '@/interfaces'
import { ref } from 'vue'

defineProps<{
  trade: LiveTrade
}>()

const selectedPlan = ref<null | ScalePlan>(null)
const isFormOpen = ref(false)
const formType = ref<'edit' | 'execute' | null>(null)

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
        <ScalePlanHoverCard :trade="trade" @open-form="openForm" />
      </div>
    </PopoverAnchor>
    <PopoverContent side="bottom" align="start">
      <ScalePlanQuickEdit
        v-if="selectedPlan && formType === 'edit'"
        :scalePlan="selectedPlan"
        :trade="trade"
        @close="closeEditForm"
      />
      <TradeExecutionForm v-if="selectedPlan && formType === 'execute'" :scalePlan="selectedPlan" />
    </PopoverContent>
  </Popover>
</template>
