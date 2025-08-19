<script setup lang="ts">
import { ref, computed } from 'vue'
import { useFormatters, useScalePlanMutationService } from '@/composables'
import type { LiveTrade, ScalePlan } from '@/interfaces'

const { formatCurrency, formatTradeDate } = useFormatters()
const { deleteMutation } = useScalePlanMutationService()
const props = defineProps<{
  trade: LiveTrade
  plan: ScalePlan
  idx: number
}>()

const formatValue = (kind: string, value?: number) =>
  typeof value === 'number' ? (kind === 'percent' ? `${value}%` : `${value} shares`) : '—'

const isReached = (current: number, target?: number | null) =>
  typeof target === 'number' && Number.isFinite(target) && current >= target

// Local disclosure state
const hoverOpen = ref(false)
const menuOpen = ref(false)
const confirmOpen = ref(false)
const cardOpen = computed(() => hoverOpen.value || menuOpen.value || confirmOpen.value)

const onUpdateHover = (v: boolean) => {
  hoverOpen.value = v
}

const onConfirmDelete = async (planId: string) => {
  console.log('Delete scale plan', {
    tradeId: props.trade?.id,
    planId,
    idx: props.idx,
  })
  await deleteMutation.mutateAsync(planId, {
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
          isReached(props.trade.currentPrice, props.plan.targetPrice)
            ? 'bg-green-50 text-green-700 border-green-200'
            : 'bg-gray-50 text-gray-700 border-gray-200'
        "
        :aria-describedby="`sp-${props.idx}-title`"
      >
        T{{ props.idx + 1 }}: {{ formatCurrency(props.plan.targetPrice ?? 0) }}
        <span v-if="isReached(props.trade.currentPrice, props.plan.targetPrice)" class="ml-1"
          >✓</span
        >
        <span class="sr-only">
          {{
            isReached(props.trade.currentPrice, props.plan.targetPrice)
              ? '(reached)'
              : '(not reached)'
          }}
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
          <DropdownMenuItem> Execute Plan </DropdownMenuItem>
          <DropdownMenuItem> Edit Plan </DropdownMenuItem>
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
                :hidden="props.plan.status !== 'planned'"
                class="text-red-600"
                @click.stop="confirmOpen = true"
              >
                Delete Plan
              </DropdownMenuItem>
            </AlertDialogTrigger>
            <AlertDialogContent>
              <AlertDialogHeader>
                <AlertDialogTitle
                  >Delete
                  {{ props.plan.label?.trim() || `Plan T${props.idx + 1}` }}?</AlertDialogTitle
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
                  @click="onConfirmDelete(props.plan.id)"
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
          <h4 :id="`sp-${props.idx}-title`" class="text-sm font-semibold">
            {{ props.plan.label?.trim() || `Plan ${props.idx + 1}` }}
          </h4>
          <Badge
            class="rounded-full bg-gray-100 text-gray-700 px-2 py-0.5 text-[11px] font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
          >
            {{ props.plan.status }}
          </Badge>
        </div>

        <div class="my-2 border-t border-gray-200"></div>

        <div class="flex flex-wrap gap-1.5 text-[11px] mb-3">
          <span class="rounded-full bg-gray-100 px-2 py-0.5"
            >Order: {{ props.plan.orderType }}</span
          >
          <span class="rounded-full bg-gray-100 px-2 py-0.5">Kind: {{ props.plan.kind }}</span>
          <span class="rounded-full bg-gray-100 px-2 py-0.5">
            Value: {{ formatValue(props.plan.kind as string, props.plan.value) }}
          </span>
        </div>

        <div class="grid grid-cols-2 gap-2 text-sm mt-2">
          <div v-if="props.plan.entryPrice != null" class="rounded bg-gray-50 p-2">
            <p class="text-xs text-gray-600">Entry</p>
            <p class="font-medium">{{ formatCurrency(props.plan.entryPrice) }}</p>
          </div>
          <div v-if="props.plan.targetPrice != null" class="rounded bg-gray-50 p-2">
            <p class="text-xs text-gray-600">Target</p>
            <p class="font-medium">{{ formatCurrency(props.plan.targetPrice) }}</p>
          </div>
          <div v-if="props.plan.stopPrice != null" class="rounded bg-gray-50 p-2">
            <p class="text-xs text-gray-600">Stop</p>
            <p class="font-medium">{{ formatCurrency(props.plan.stopPrice) }}</p>
          </div>
          <div v-if="props.plan.limitPrice != null" class="rounded bg-gray-50 p-2">
            <p class="text-xs text-gray-600">Limit</p>
            <p class="font-medium">{{ formatCurrency(props.plan.limitPrice) }}</p>
          </div>
        </div>

        <div v-if="props.plan.goodTillDate" class="text-xs text-gray-600">
          Good till: <span class="font-medium">{{ formatTradeDate(props.plan.goodTillDate) }}</span>
        </div>

        <div v-if="props.plan.notes" class="text-sm">
          <p class="text-xs text-gray-600 mb-1">Notes</p>
          <p class="leading-snug">{{ props.plan.notes }}</p>
        </div>
      </div>
    </HoverCardContent>
  </HoverCard>
</template>
