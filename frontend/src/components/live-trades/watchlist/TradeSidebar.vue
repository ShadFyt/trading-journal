<script lang="ts" setup>
import { useTradeFetchingService, useProvideTradeActions } from '@/composables'
import { Icon } from '@iconify/vue'
import type { Trade } from '@/interfaces'
import { ScalePlanTypeEnum } from '@/enums'
import TradeSideBarHeader from '@/components/live-trades/watchlist/TradeSideBarHeader.vue'
import { useToggle } from '@vueuse/core'
import { useFuse } from '@vueuse/integrations/useFuse'

const [isExecutionFormOpen, toggleExecutionFormExpanded] = useToggle(false)
const [isTradeFormOpen, toggleTradeFormExpanded] = useToggle(false)

const props = defineProps<{
  isOpen?: boolean
}>()

const { watchlist } = useTradeFetchingService()
const selectedTrade = ref<Trade | null>(null)

const searchQuery = ref('')

const { results } = useFuse(searchQuery, watchlist, {
  fuseOptions: {
    keys: ['symbol'],
    threshold: 0.3,
    includeScore: true,
  },
  matchAllWhenSearchEmpty: true,
})

const filteredWatchlist = computed(() => {
  const searchResults = results.value.map((result) => result.item)

  if (selectedTrade.value && !searchResults.some((trade) => trade.id === selectedTrade.value?.id)) {
    return [selectedTrade.value, ...searchResults]
  }

  return searchResults
})

const entryPlan = computed(() => {
  return selectedTrade.value?.scalePlans.find((p) => p.planType === ScalePlanTypeEnum.enum.ENTRY)
})

const handleTradeSelect = (trade: Trade) => {
  if (isExecutionFormOpen.value) return
  selectedTrade.value = trade
}

const handleTradeFormOpen = () => {
  selectedTrade.value = null
  toggleTradeFormExpanded(true)
}

useProvideTradeActions({
  openExecutionForm: () => toggleExecutionFormExpanded(true),
  openTradeForm: () => toggleTradeFormExpanded(true),
  clearSelectedTrade: () => (selectedTrade.value = null),
})
</script>

<template>
  <aside
    :class="[
      'fixed inset-y-0 right-0 z-40 w-full lg:w-100 h-screen bg-gray-900 border-r border-gray-800 flex flex-col transform transition-transform duration-300 ease-in-out lg:relative lg:translate-x-0',
      props.isOpen ? 'translate-x-0' : 'translate-x-full lg:translate-x-0',
    ]"
  >
    <template v-if="isTradeFormOpen">
      <TradeForm :trade="selectedTrade" @close="() => toggleTradeFormExpanded(false)" />
    </template>
    <template v-else>
      <TradeSideBarHeader
        @open-trade-form="handleTradeFormOpen"
        v-model:search-query="searchQuery"
      />

      <div class="flex-1 flex flex-col min-h-0">
        <div v-if="!filteredWatchlist?.length" class="text-center py-12">
          <div class="text-6xl mb-4">📈</div>
          <h3 class="text-xl font-semibold text-gray-900 mb-2">No Watchlist Trades</h3>
          <p class="text-gray-600">Add trades to your watchlist to see them here.</p>
        </div>
        <ScrollArea
          v-else
          :class="selectedTrade && !isExecutionFormOpen ? 'flex-1 max-h-[50vh]' : 'flex-1'"
        >
          <div class="p-2">
            <div
              v-for="trade in filteredWatchlist"
              :key="trade.id"
              :class="[
                'p-3 rounded-lg transition-all mb-1',
                !isExecutionFormOpen ? 'cursor-pointer hover:bg-gray-800' : '',
                selectedTrade?.id === trade.id ? 'bg-gray-800 ring-1 ring-blue-500' : '',
              ]"
              @click="handleTradeSelect(trade)"
            >
              <TradePriceDetail :trade />
            </div>
          </div>
        </ScrollArea>
      </div>

      <div class="flex-1 max-h-[50vh] border-t border-gray-700">
        <TradeExecutionForm
          v-if="isExecutionFormOpen && entryPlan"
          :scalePlan="entryPlan"
          :extraClass="'p-3 m-2 bg-gray-800/50 border-none flex flex-col flex-1 min-h-0'"
          @close="() => toggleExecutionFormExpanded(false)"
        >
          <template #header>
            <CardHeader class="bg-emerald-900 px-4 py-3 -m-3 mb-3 rounded-t-lg">
              <CardTitle class="text-base text-slate-100 flex justify-between">
                <p class="font-medium text-md text-emerald-300">
                  Execute Entry Plan for {{ selectedTrade?.symbol }}
                </p>
                <Icon
                  icon="lucide:square-x"
                  width="24"
                  height="24"
                  class="cursor-pointer text-red-400 hover:text-red-300"
                  @click="isExecutionFormOpen = false"
                />
              </CardTitle>
            </CardHeader>
          </template>
        </TradeExecutionForm>
        <TradeDetails
          v-if="selectedTrade && !isExecutionFormOpen"
          :selected-trade="selectedTrade"
        />
      </div>
    </template>
  </aside>
</template>
