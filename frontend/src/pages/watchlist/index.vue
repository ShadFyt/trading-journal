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
import type { Watchlist } from '@/interfaces/watchlist.type'

const filter = ref('all')

const watchlist = ref<Watchlist>([
  {
    symbol: 'CCL',
    status: 'waiting',
    setupType: 'Ascending Triangle Breakout + Golden Cross Formation',
    rating: 8,
    entryRange: '$22.50-$23.00',
    stop: 21.5,
    target: 25.5,
    rr: 2.5,
    catalyst: 'Citigroup raised PT to $28 from $25',
    ideaDate: '',
  },
  {
    symbol: 'HIMS',
    status: 'invalidated',
    setupType: 'Upside Continuation',
    rating: 6,
    entryRange: '$50',
    stop: 44,
    target: 58,
    rr: 1.33,
    ideaDate: '',
  },
  {
    symbol: 'OKLO',
    status: 'waiting',
    setupType: 'Double Top short',
    rating: 6,
    entryRange: 'Close < $47.00 (Vol 3-5M+)',
    stop: 48.5,
    target: 38,
    rr: 1.6,
    ideaDate: '',
  },
  {
    symbol: 'GLXY',
    status: 'invalidated',
    setupType: 'Double Top short',
    rating: 8.5,
    entryRange: 'Break < $18.90',
    stop: 20.5,
    target: 15.5,
    rr: 2.3,
    ideaDate: 'June 7',
  },
  {
    symbol: 'XBI',
    status: 'waiting',
    setupType: 'Breakout',
    rating: 7.5,
    entryRange: 'Break > 84.30',
    stop: 82,
    target: 87,
    rr: 2.3,
    ideaDate: 'June 7',
  },
])

const filteredWatchlist = computed(() => {
  if (filter.value === 'all') return watchlist.value
  return watchlist.value.filter((t) => t.status.toLowerCase() === filter.value)
})
</script>

<template>
  <div class="p-4 max-w-7xl mx-auto">
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
        <CardContent class="p-6">
          <div class="flex justify-between items-center mb-2">
            <div class="flex items-center gap-2">
              <span class="text-2xl">💹</span>
              <h2 class="text-2xl font-bold text-blue-700 tracking-wide">{{ trade.symbol }}</h2>
            </div>
            <Badge
              class="capitalize px-3 py-1 text-xs rounded-full border font-semibold"
              :class="statusBadgeClass[trade.status]"
            >
              {{ trade.status }}
            </Badge>
          </div>
          <p class="text-xs text-gray-400 mb-3 italic">{{ trade.setupType }}</p>

          <div class="grid grid-cols-2 gap-x-4 gap-y-1 text-sm mb-2">
            <p><span class="font-semibold">Entry Range:</span> {{ trade.entryRange }}</p>
            <p><span class="font-semibold">Stop:</span> ${{ trade.stop }}</p>
            <p><span class="font-semibold">Target:</span> ${{ trade.target }}</p>
            <p><span class="font-semibold">Risk/Reward:</span> 1:{{ trade.rr }}</p>
            <p><span class="font-semibold">Rating:</span> {{ trade.rating }}/10</p>
            <p v-if="trade.catalyst" class="col-span-2">
              <span class="font-semibold">Catalyst:</span> {{ trade.catalyst }}
            </p>
          </div>

          <div class="mt-3 flex justify-between text-xs text-gray-500">
            <span>💡 {{ trade.ideaDate }}</span>
          </div>
        </CardContent>
      </Card>
    </div>
    <FabRoutingButton
      to="/watchlist/new-entry"
      message="Add New Entry"
      position="bottom-right"
      size="m"
    />
  </div>
</template>
