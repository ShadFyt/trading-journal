<script setup lang="ts">
import type { LiveTrade, ScalePlan } from '@/interfaces'
import { computed, ref } from 'vue'
import { sharesFromPercent } from '@/utils'
import { useScalePlanMutations, useTradeExecutionMutations } from '@/composables'
import { Icon } from '@iconify/vue'
import ExecutionSelector from '../../trade-execution/ExecutionSelector.vue'
import { ScalePlanStatusEnum } from '@/enums'
const { deletePlanMutation } = useScalePlanMutations()
const { deleteExecutionMutation } = useTradeExecutionMutations()

const { plan, trade, idx } = defineProps<{
  trade: LiveTrade
  plan: ScalePlan
  idx: number
}>()

const emit = defineEmits<{
  (e: 'open-form', plan: ScalePlan, type: 'execute' | 'edit'): []
}>()

// Local disclosure state
const hoverOpen = ref(false)
const menuOpen = ref(false)
const confirmOpen = ref(false)
const selectedExecutionIds = ref<string[]>([])
const cardOpen = computed(() => hoverOpen.value || menuOpen.value || confirmOpen.value)

const isReached = computed(() => {
  const shares =
    plan.kind === 'percent' ? sharesFromPercent(trade.positionSize, plan.value).shares : plan.value
  const qty = plan.executions.reduce((total, exec) => total + exec.qty, 0)
  return qty === shares
})

const isMultipleExecutions = computed(() => plan.executions.length > 1)

const onUpdateHover = (v: boolean) => {
  hoverOpen.value = v
}

const onConfirmDelete = async () => {
  const onSettled = () => {
    menuOpen.value = false
    confirmOpen.value = false
  }

  if (!isReached.value) {
    await deletePlanMutation.mutateAsync(plan.id, {
      onSettled,
    })
    return
  }

  // For multiple executions, ensure at least one is selected
  if (isMultipleExecutions.value && selectedExecutionIds.value.length === 0) {
    return // Don't proceed if no executions selected
  }

  const ids = isMultipleExecutions.value ? selectedExecutionIds.value : [plan.executions[0].id]
  await deleteExecutionMutation.mutateAsync({ ids }, { onSettled })
}

const actionMenuBind = computed(() => {
  const planBindings = {
    alertDescription: `This action cannot be undone. This will permanently remove this scale plan from the trade`,
    alertTitle: plan.label.trim(),
    triggerText: 'Delete Plan',
  }
  const executionBindings = {
    alertDescription: `This action cannot be undone. This will permanently remove all executions from this scale plan`,
    alertTitle: plan.label.trim() + ' Executions',
    triggerText: 'Delete Executions',
  }

  return {
    menuOpen: menuOpen.value,
    confirmOpen: confirmOpen.value,
    'onUpdate:menuOpen': (v: boolean) => (menuOpen.value = v),
    'onUpdate:confirmOpen': (v: boolean) => (confirmOpen.value = v),
    onDelete: onConfirmDelete,
    ...(isReached.value ? executionBindings : planBindings),
  }
})
</script>

<template>
  <HoverCard :open="cardOpen" :open-delay="150" :close-delay="100" @update:open="onUpdateHover">
    <ShowScalePlan :plan :idx="idx" :is-reached="isReached" />

    <HoverCardContent class="relative w-80 max-w-[90vw] p-2.5" align="start">
      <ActionMenu v-bind="actionMenuBind">
        <template v-if="!isReached" #extra-actions>
          <DropdownMenuItem @select="emit('open-form', plan, 'execute')">
            <Icon icon="lucide:circle-fading-arrow-up" width="24" height="24" />Execute Plan
          </DropdownMenuItem>
          <DropdownMenuItem @select="emit('open-form', plan, 'edit')">
            <Icon icon="lucide:edit" width="24" height="24" />edit
          </DropdownMenuItem>
        </template>
        <template v-if="isMultipleExecutions" #dialog-content>
          <ExecutionSelector
            :executions="plan.executions"
            :open="confirmOpen"
            @update:selected="selectedExecutionIds = $event"
          />
        </template>
      </ActionMenu>

      <TradeExecutionContent
        v-if="
          plan.status === ScalePlanStatusEnum.enum.FILLED ||
          plan.status === ScalePlanStatusEnum.enum.PARTIALLY_FILLED
        "
        :trade
        :plan
        :idx
      />
      <ScalePlanContent v-else :trade :plan :idx />
    </HoverCardContent>
  </HoverCard>
</template>
