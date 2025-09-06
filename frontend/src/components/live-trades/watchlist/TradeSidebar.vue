<script lang="ts" setup>
import { useLiveTradeFetchingService } from '@/composables'
import { Icon } from '@iconify/vue'
import type { LiveTrade } from '@/interfaces'
import { ScalePlanTypeEnum } from '@/enums'

const props = defineProps<{
  isOpen?: boolean
}>()

const { watchlist } = useLiveTradeFetchingService()
const selectedTrade = ref<LiveTrade | null>(null)
const isExecutionFormOpen = ref(false)

const entryPlan = computed(() => {
  return selectedTrade.value?.scalePlans.find((p) => p.planType === ScalePlanTypeEnum.enum.ENTRY)
})

const handleTradeSelect = (trade: LiveTrade) => {
  selectedTrade.value = trade
}

const openExecutionForm = () => (isExecutionFormOpen.value = true)
</script>

<template>
  <aside
    :class="[
      'fixed inset-y-0 right-0 z-40 w-full lg:w-80 h-screen bg-gray-900 border-r border-gray-800 flex flex-col transform transition-transform duration-300 ease-in-out lg:relative lg:translate-x-0',
      props.isOpen ? 'translate-x-0' : 'translate-x-full lg:translate-x-0'
    ]"
  >
    <div class="p-4 border-b border-gray-800">
      <h2 class="text-lg font-semibold text-white mb-3">Watchlist</h2>
      <div class="relative">
        <Input
          placeholder="Search symbols..."
          class="pl-10 bg-gray-800 border-gray-700 text-white placeholder-gray-400"
        />
      </div>
    </div>
    <div class="flex-1 flex flex-col min-h-0">
      <ScrollArea class="flex-1">
        <div class="p-2">
          <div
            v-for="trade in watchlist"
            :key="trade.id"
            :class="[
              'p-3 rounded-lg cursor-pointer transition-all hover:bg-gray-800 mb-1',
              selectedTrade?.id === trade.id ? 'bg-gray-800 ring-1 ring-blue-500' : '',
            ]"
            @click="handleTradeSelect(trade)"
          >
            <TradePriceDetail :trade />
          </div>
        </div>
      </ScrollArea>
    </div>
    <TradeExecutionForm
      v-if="isExecutionFormOpen && entryPlan"
      :scalePlan="entryPlan"
      :extraClass="'p-3 m-2 bg-gray-800/50 border-none text-gray-100'"
    >
      <template #header>
        <div class="flex justify-between">
          <p class="text-xs font-semibold text-center mb-3">
            Execute Entry Plan for {{ selectedTrade?.symbol }}
          </p>
          <Icon
            icon="lucide:square-x"
            width="24"
            height="24"
            class="cursor-pointer text-red-400 hover:text-red-300"
            @click="isExecutionFormOpen = false"
          />
        </div>
      </template>
    </TradeExecutionForm>
    <TradeDetails
      v-if="selectedTrade && !isExecutionFormOpen"
      :selected-trade="selectedTrade"
      @open-execution-form="openExecutionForm"
    />
  </aside>
</template>
