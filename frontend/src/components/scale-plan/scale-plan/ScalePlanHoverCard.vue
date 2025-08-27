<script setup lang="ts">
import type { LiveTrade, ScalePlan } from '@/interfaces'
import { computed } from 'vue'
import { sharesFromPercent } from '@/utils'

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
  emit('open-form', plan, type)
}
</script>

<template>
  <HoverCard :open="cardOpen" :open-delay="150" :close-delay="100" @update:open="onUpdateHover">
    <ShowScalePlan :plan :idx="idx" :is-reached="isReached" />

    <HoverCardContent class="relative w-80 max-w-[90vw] p-2.5" align="start">
      <ScalePlanMenu
        :plan
        :idx
        v-model:menu-open="menuOpen"
        v-model:confirm-open="confirmOpen"
        @open-form="onOpenForm"
      />

      <ScalePlanContent :trade :plan :idx />
    </HoverCardContent>
  </HoverCard>
</template>
