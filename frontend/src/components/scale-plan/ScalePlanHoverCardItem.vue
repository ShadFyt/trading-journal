<script setup lang="ts">
import { ref, computed } from 'vue'
import { Icon } from '@iconify/vue'
import { useFormatters, useScalePlanMutations } from '@/composables'
import type { LiveTrade, ScalePlan } from '@/interfaces'

const { formatCurrency, formatTradeDate } = useFormatters()
const { deletePlanMutation } = useScalePlanMutations()
const { plan, trade, idx } = defineProps<{
  trade: LiveTrade
  plan: ScalePlan
  idx: number
}>()

const formatValue = (kind: string, value?: number) =>
  typeof value === 'number' ? (kind === 'percent' ? `${value}%` : `${value} shares`) : '—'

const isReached = computed(() => {
  const qty = plan.executions.reduce((total, exec) => total + exec.qty, 0)
  return qty === trade.positionSize
})

// Local disclosure state
const hoverOpen = ref(false)
const menuOpen = ref(false)
const confirmOpen = ref(false)
const cardOpen = computed(() => hoverOpen.value || menuOpen.value || confirmOpen.value)

const onUpdateHover = (v: boolean) => {
  hoverOpen.value = v
}

const onConfirmDelete = async (planId: string) => {
  await deletePlanMutation.mutateAsync(planId, {
    onSettled() {
      menuOpen.value = false
      confirmOpen.value = false
    },
  })
}
</script>

<template>
  <HoverCard :open="cardOpen" :open-delay="150" :close-delay="100" @update:open="onUpdateHover">
    <HoverCardTrigger as-child>
      <Badge
        role="button"
        tabindex="0"
        class="text-xs focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
        :class="
          isReached
            ? 'bg-green-50 text-green-700 border-green-200'
            : 'bg-gray-50 text-gray-700 border-gray-200'
        "
        :aria-describedby="`sp-${trade.id}-title`"
      >
        T{{ idx + 1 }}: {{ formatCurrency(plan.targetPrice ?? 0) }}
        <span v-if="isReached" class="ml-1">✓</span>
        <span class="sr-only">
          {{ isReached ? '(reached)' : '(not reached)' }}
        </span>
      </Badge>
    </HoverCardTrigger>

    <HoverCardContent class="relative w-80 max-w-[90vw] p-2.5" align="start">
      <DropdownMenu
        as-child
        :open="menuOpen || confirmOpen"
        @update:open="
          (v: boolean) => {
            menuOpen = v
          }
        "
      >
        <DropdownMenuTrigger class="absolute top-1 right-1">
          <Button
            variant="ghost"
            size="sm"
            aria-label="Open trade menu"
            aria-haspopup="menu"
            class="h-11 w-11 p-0 rounded-full min-w-[44px] min-h-[44px] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2"
          >
            ⋯
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent side="bottom" align="end" :avoidCollisions="false">
          <DropdownMenuItem @select="$emit('open-form', plan, 'execute')">
            <Icon icon="lucide:circle-fading-arrow-up" width="24" height="24" />Execute Plan
          </DropdownMenuItem>
          <DropdownMenuItem @select="$emit('open-form', plan, 'edit')">
            <Icon icon="lucide:edit" width="24" height="24" />edit
          </DropdownMenuItem>
          <AlertDialog
            :open="confirmOpen"
            @update:open="
              (v: boolean) => {
                confirmOpen = v
              }
            "
          >
            <AlertDialogTrigger as-child>
              <DropdownMenuItem
                :hidden="plan.status !== 'planned'"
                class="text-red-600"
                @click.stop="confirmOpen = true"
                ><Icon icon="lucide:trash-2" width="24" height="24" />
                Delete Plan
              </DropdownMenuItem>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle
                  >Delete {{ plan.label?.trim() || `Plan T${idx + 1}` }}?</AlertDialogTitle
                >
                <AlertDialogDescription>
                  This action cannot be undone. This will permanently remove this scale plan from
                  the trade.
                </AlertDialogDescription>
              </AlertDialogHeader>
              <AlertDialogFooter>
                <AlertDialogCancel @click="confirmOpen = false">Cancel</AlertDialogCancel>
                <AlertDialogAction
                  class="bg-red-600 hover:bg-red-700 text-white"
                  @click="onConfirmDelete(plan.id)"
                >
                  Delete
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </DropdownMenuContent>
      </DropdownMenu>

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
