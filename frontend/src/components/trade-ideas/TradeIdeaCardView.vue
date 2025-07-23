<script setup lang="ts">
import { ref, computed } from 'vue'
import { Card, CardContent } from '@/components/ui/card'
import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
} from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'
import { statusOptions, statusBadgeClass } from '@/shared/status'
import { useTradeIdeaFetchingService } from '@/composables'
import type { TradeIdea } from '@/interfaces/trade-idea.type'
import { useFormatters } from '@/composables/useFormatters'

const { tradeIdeas: watchlist, isLoading } = useTradeIdeaFetchingService()
const { formatTradeDate, formatEntryPrice } = useFormatters()

const filter = ref('all')
const isOpen = ref(false)
const isFormOpen = ref(false)
const selectedTrade = ref<TradeIdea | null>(null)

const filteredWatchlist = computed(() => {
  if (isLoading.value || !watchlist.value) return []
  if (filter.value === 'all') return watchlist.value
  return watchlist.value?.filter((t) => t.status.toLowerCase() === filter.value)
})

const getStatusBadgeProps = computed(() => (status: string) => ({
  class: [
    'cursor-pointer hover:opacity-80 capitalize px-3 py-1 text-xs rounded-full border font-semibold',
    statusBadgeClass[status],
  ],
}))

const handleDialogOpen = (idea: TradeIdea) => {
  selectedTrade.value = idea
  isOpen.value = true
}
const handleDialogClose = () => {
  isOpen.value = false
  selectedTrade.value = null
}
const handleFormOpen = (idea: TradeIdea) => {
  isFormOpen.value = true
  selectedTrade.value = idea
}
const handleFormClose = () => {
  isFormOpen.value = false
  selectedTrade.value = null
}
</script>

<template>
  <main class="p-4 max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-6">
      <h1 class="text-3xl font-extrabold tracking-tight text-blue-800 drop-shadow-sm">
        Swing Trading Watchlist
      </h1>
      <Select
        v-model="filter"
        class="w-56 shadow-md rounded-lg border-blue-200 border-2 focus:ring-2 focus:ring-blue-400"
      >
        <SelectTrigger>
          <SelectValue placeholder="Filter by Status" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem v-for="option in statusOptions" :key="option.value" :value="option.value">
            {{ option.label }}
          </SelectItem>
        </SelectContent>
      </Select>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <Card
        v-for="trade in filteredWatchlist"
        :key="trade.symbol"
        class="relative transition-shadow hover:shadow-2xl border border-gray-200 rounded-xl bg-white shadow-sm overflow-hidden group animate-fadein"
      >
        <CardHeader>
          <DropdownMenu>
            <DropdownMenuTrigger class="absolute top-2 right-2">
              <Button variant="ghost" size="sm">⋯</Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent side="bottom" align="end" :avoidCollisions="false">
              <DropdownMenuItem @click="handleFormOpen(trade)"> Edit </DropdownMenuItem>
              <DropdownMenuItem class="text-red-600" @click="handleDialogOpen(trade)"
                >Delete</DropdownMenuItem
              >
            </DropdownMenuContent>
          </DropdownMenu>
        </CardHeader>
        <CardContent>
          <div class="flex justify-between items-center mb-2">
            <div class="flex items-center gap-2">
              <span class="text-2xl">💹</span>
              <h2 class="text-2xl font-bold text-blue-700 tracking-wide">{{ trade.symbol }}</h2>
            </div>
            <Badge v-bind="getStatusBadgeProps(trade.status)">{{ trade.status }}</Badge>
          </div>
          <p class="text-xs text-gray-400 mb-3 italic">{{ trade.setup }}</p>

          <div class="grid grid-cols-2 gap-x-4 gap-y-1 text-sm mb-2">
            <p>
              <span class="font-semibold">Entry:</span>
              {{ formatEntryPrice(trade.entryMin, trade.entryMax) }}
            </p>
            <p><span class="font-semibold">Stop:</span> ${{ trade.stop }}</p>
            <p v-for="(target, idx) in trade.targetPrices" :key="target">
              <span class="font-semibold">Target {{ idx + 1 }}:</span> ${{ target }}
            </p>
            <p><span class="font-semibold">Risk/Reward:</span> 1:{{ trade.rrRatio }}</p>
            <p><span class="font-semibold">Rating:</span> {{ trade.rating }}/10</p>
            <p v-if="trade.catalysts" class="col-span-2">
              <span class="font-semibold">Catalyst:</span> {{ trade.catalysts }}
            </p>
            <p v-if="trade.notes" class="col-span-2">
              <span class="font-semibold">Notes:</span> {{ trade.notes }}
            </p>
          </div>

          <div class="mt-3 flex justify-between text-xs text-gray-500">
            <span class="text-xs text-gray-400">{{
              formatTradeDate(trade.ideaDate.toString())
            }}</span>
          </div>
        </CardContent>
      </Card>
    </div>
  </main>
  <ConfirmationDialog
    v-if="selectedTrade"
    :open="isOpen"
    :selectedTrade="selectedTrade"
    @close="handleDialogClose"
  />
  <TradeIdeaForm
    v-if="selectedTrade"
    :selectedTrade="selectedTrade"
    :isOpen="isFormOpen"
    :close="handleFormClose"
  />
</template>
