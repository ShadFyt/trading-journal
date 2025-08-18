<script setup lang="ts">
import type { LiveTrade } from '@/interfaces'
import { useFormatters } from '@/composables'
import { computed } from 'vue'

const { trade } = defineProps<{
  trade: LiveTrade
}>()

const { formatCurrency, formatTradeDate } = useFormatters()
const plans = computed(() => trade.scalePlans ?? [])

const formatValue = (kind: string, value?: number) =>
  typeof value === 'number' ? (kind === 'percent' ? `${value}%` : `${value} shares`) : '—'

const isReached = (current: number, target?: number | null) =>
  typeof target === 'number' && Number.isFinite(target) && current >= target
</script>

<template>
  <div class="flex flex-wrap gap-1">
    <HoverCard
      v-for="(plan, idx) in plans"
      :key="plan.id ?? idx"
      :open-delay="150"
      :close-delay="100"
    >
      <HoverCardTrigger as-child>
        <Badge
          role="button"
          tabindex="0"
          class="text-xs focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
          :class="
            isReached(trade.currentPrice, plan.targetPrice)
              ? 'bg-green-50 text-green-700 border-green-200'
              : 'bg-gray-50 text-gray-700 border-gray-200'
          "
          :aria-describedby="`sp-${idx}-title`"
        >
          T{{ idx + 1 }}: {{ formatCurrency(plan.targetPrice ?? 0) }}
          <span v-if="isReached(trade.currentPrice, plan.targetPrice)" class="ml-1">✓</span>
          <span class="sr-only">
            {{ isReached(trade.currentPrice, plan.targetPrice) ? '(reached)' : '(not reached)' }}
          </span>
        </Badge>
      </HoverCardTrigger>

      <HoverCardContent class="w-80 max-w-[90vw]">
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <h4 :id="`sp-${idx}-title`" class="text-sm font-semibold">
              {{ plan.label?.trim() || `Plan ${idx + 1}` }}
            </h4>
          </div>

          <div class="flex flex-wrap gap-2 text-xs">
            <span class="rounded bg-gray-100 px-2 py-0.5">Order: {{ plan.orderType }}</span>
            <span class="rounded bg-gray-100 px-2 py-0.5">Kind: {{ plan.kind }}</span>
            <span class="rounded bg-gray-100 px-2 py-0.5">
              Value: {{ formatValue(plan.kind as string, plan.value) }}
            </span>
          </div>

          <div class="grid grid-cols-2 gap-2 text-sm">
            <div v-if="plan.entryPrice != null" class="rounded border p-2">
              <p class="text-xs text-gray-600">Entry</p>
              <p class="font-medium">{{ formatCurrency(plan.entryPrice) }}</p>
            </div>
            <div v-if="plan.targetPrice != null" class="rounded border p-2">
              <p class="text-xs text-gray-600">Target</p>
              <p class="font-medium">{{ formatCurrency(plan.targetPrice) }}</p>
            </div>
            <div v-if="plan.stopPrice != null" class="rounded border p-2">
              <p class="text-xs text-gray-600">Stop</p>
              <p class="font-medium">{{ formatCurrency(plan.stopPrice) }}</p>
            </div>
            <div v-if="plan.limitPrice != null" class="rounded border p-2">
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
  </div>
</template>
