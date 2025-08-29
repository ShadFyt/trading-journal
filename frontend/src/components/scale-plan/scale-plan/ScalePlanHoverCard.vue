<script setup lang="ts">
import type { LiveTrade, ScalePlan } from '@/interfaces'
import { computed } from 'vue'
import { sharesFromPercent } from '@/utils'
import { useScalePlanMutations } from '@/composables'
const { deletePlanMutation } = useScalePlanMutations()

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
const cardOpen = computed(() => hoverOpen.value || menuOpen.value || confirmOpen.value)

const isReached = computed(() => {
  const shares =
    plan.kind === 'percent' ? sharesFromPercent(trade.positionSize, plan.value).shares : plan.value
  const qty = plan.executions.reduce((total, exec) => total + exec.qty, 0)
  return qty === shares
})

const onUpdateHover = (v: boolean) => {
  hoverOpen.value = v
}

const onOpenForm = (type: 'execute' | 'edit') => {
  console.info('testing')
  emit('open-form', plan, type)
}

const onConfirmDelete = async () => {
  await deletePlanMutation.mutateAsync(plan.id, {
    onSettled() {
      menuOpen.value = false
      confirmOpen.value = false
    },
  })
}

const actionMenuBind = computed(() => ({
  menuOpen: menuOpen.value,
  confirmOpen: confirmOpen.value,
  'onUpdate:menuOpen': (v: boolean) => (menuOpen.value = v),
  'onUpdate:confirmOpen': (v: boolean) => (confirmOpen.value = v),

  title: 'test',
  alertTitle: plan.label.trim(),
  domain: 'scale plan',

  onDelete: onConfirmDelete,
  onOpenForm: (type: 'execute' | 'edit') => onOpenForm(type),
}))
</script>

<template>
  <HoverCard :open="cardOpen" :open-delay="150" :close-delay="100" @update:open="onUpdateHover">
    <ShowScalePlan :plan :idx="idx" :is-reached="isReached" />

    <HoverCardContent class="relative w-80 max-w-[90vw] p-2.5" align="start">
      <ActionMenu v-bind="actionMenuBind" />

      <TradeExecutionContent v-if="isReached" :trade :plan :idx />
      <ScalePlanContent v-else :trade :plan :idx />
    </HoverCardContent>
  </HoverCard>
</template>
