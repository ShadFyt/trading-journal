<script lang="ts" setup>
import type { ScalePlan, Trade } from '@/interfaces'
import { useFormatters, useTradeMetrics } from '@/composables'
import { ScalePlanTypeEnum, ScalePlanStatusEnum } from '@/enums'

const BILLION = 1_000
const TRILLION = BILLION * 1_000
const DECIMAL_PLACES = 2

const { formatCurrency } = useFormatters()
const props = defineProps<{ selectedTrade: Trade }>()
const { entryPlan } = useTradeMetrics(toRef(props, 'selectedTrade'))

const targetPlans = computed(() => {
  return props.selectedTrade.scalePlans
    .filter(
      (plan) =>
        plan.planType === ScalePlanTypeEnum.enum.TARGET &&
        plan.status !== ScalePlanStatusEnum.enum.CANCELLED &&
        plan.targetPrice != null,
    )
    .sort((a, b) => (a.targetPrice || 0) - (b.targetPrice || 0))
})

const formatMarketCap = (cap?: number) => {
  if (!cap) return 0
  if (cap >= TRILLION) {
    return `$${(cap / TRILLION).toFixed(DECIMAL_PLACES)}T`
  } else if (cap >= BILLION) {
    return `$${(cap / BILLION).toFixed(DECIMAL_PLACES)}B`
  } else {
    return `$${cap.toFixed(DECIMAL_PLACES)}M`
  }
}

const calculateRRRatio = (targetPlan: ScalePlan) => {
  const entryPrice = entryPlan.value.entryPriceAvg
  const targetPrice = targetPlan.targetPrice || 0
  const stopLoss = entryPlan.value.stopLoss

  if (entryPrice === 0 || stopLoss === 0) return 0

  const reward = targetPrice - entryPrice
  const risk = entryPrice - stopLoss

  return Math.round((reward / risk) * 100) / 100
}
</script>

<template>
  <div class="h-full flex flex-col">
    <Card class="p-3 m-2 bg-gray-800/50 border-none flex flex-col flex-1 min-h-0">
      <TradeDetailHeader :trade="props.selectedTrade" />
      <div class="flex-1 overflow-y-auto">
        <CardContent class="pb-4">
          <div class="grid grid-cols-2 gap-x-4 gap-y-3 mb-4">
            <div>
              <p class="text-gray-400 text-xs mb-1">Last Price</p>
              <p class="text-white font-medium">
                {{ formatCurrency(props.selectedTrade.currentPrice) }}
              </p>
            </div>
            <div>
              <p class="text-gray-400 text-xs mb-1">Entry Target</p>
              <p class="text-blue-400 font-medium">{{ formatCurrency(entryPlan.entryPriceAvg) }}</p>
            </div>
            <div>
              <p class="text-gray-400 text-xs mb-1">Stop Loss</p>
              <p class="text-red-400 font-medium">{{ formatCurrency(entryPlan.stopLoss) }}</p>
            </div>
            <div>
              <p class="text-gray-400 text-xs mb-1">R/R Ratio</p>
              <p class="text-white font-medium">{{ props.selectedTrade.rrRatio }}</p>
            </div>
          </div>

          <div v-if="targetPlans.length > 0" class="mb-4">
            <p class="text-gray-400 text-xs mb-2">Price Targets</p>
            <div class="flex flex-wrap gap-2">
              <div
                v-for="(target, index) in targetPlans"
                :key="target.id"
                class="flex-1 min-w-[120px] p-2 rounded bg-gray-800/30 border border-gray-700"
              >
                <div class="text-center">
                  <p class="text-xs text-gray-400 mb-1">
                    Target {{ index + 1 }} ({{ calculateRRRatio(target) }} R/R)
                  </p>
                  <p class="text-green-400 font-medium text-sm">
                    {{ formatCurrency(target.targetPrice || 0) }}
                  </p>
                  <p v-if="target.qty" class="text-gray-400 text-xs mt-1">
                    {{ target.qty }} shares
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 gap-y-3 mb-4">
            <div>
              <p class="text-gray-400 text-xs mb-1">Timeframe</p>
              <p class="text-white font-medium">3-6 months</p>
            </div>
          </div>

          <div>
            <p class="text-gray-400 text-xs mb-2">Notes</p>
            <p class="text-gray-300 text-xs leading-relaxed">
              Strong dividend yield, pipeline expansion projects looking promising. Good entry point
              after recent pullback.
            </p>
          </div>
        </CardContent>
        <CardFooter class="border-t border-gray-700 flex items-center justify-between">
          <span v-if="props.selectedTrade.industry" class="text-blue-400 text-xs font-medium"
            >{{ props.selectedTrade.industry }}
          </span>
          <span v-if="props.selectedTrade.cap" class="text-gray-400 text-xs">
            Cap: {{ formatMarketCap(props.selectedTrade.cap) }}
          </span>
        </CardFooter>
      </div>
    </Card>
  </div>
</template>
