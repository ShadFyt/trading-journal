<script lang="ts" setup>
import { Popover, PopoverAnchor, PopoverContent } from '@/components/ui/popover'
import type { LiveTrade, ScalePlan } from '@/interfaces'
import { ref } from 'vue'

defineProps<{
  trade: LiveTrade
}>()

const selectedPlan = ref<null | ScalePlan>(null)
const isScalePlanFormOpen = ref(false)

const openEditForm = (scalePlan: ScalePlan) => {
  selectedPlan.value = scalePlan
  isScalePlanFormOpen.value = true
}

const closeEditForm = () => {
  selectedPlan.value = null
  isScalePlanFormOpen.value = false
}
</script>

<template>
  <Popover v-model:open="isScalePlanFormOpen">
    <PopoverAnchor as-child>
      <div class="mb-3">
        <div class="flex justify-between">
          <p class="text-xs font-semibold text-gray-600 uppercase tracking-wide mb-1">Targets</p>
          <ScalePlanQuickAdd :trade="trade" />
        </div>
        <ScalePlanHoverCard :trade="trade" @edit="openEditForm" />
      </div>
    </PopoverAnchor>
    <PopoverContent side="bottom" align="start">
      <ScalePlanQuickEdit v-if="selectedPlan" :scalePlan="selectedPlan" @close="closeEditForm" />
    </PopoverContent>
  </Popover>
</template>
