<script setup lang="ts">
/**
 * Returns the P/L value as a number (handles string or number, fallback 0).
 * @param trade The trade object
 * @returns number
 * @example
 * plNumber({ pl: "12.5" }) // 12.5
 * plNumber({ pl: undefined }) // 0
 */
function plNumber(trade: { pl?: string | number }) {
  const val = trade?.pl
  if (typeof val === 'number') return val
  if (typeof val === 'string') {
    const n = Number(val)
    return isNaN(n) ? 0 : n
  }
  return 0
}

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

const filter = ref('all')

const watchlist = ref([
  {
    symbol: 'CCL',
    status: 'waiting',
    setupType: 'Ascending Triangle Breakout + Golden Cross Formation',
    rating: '80/10',
    entry: '$22.50-$23.00',
    stop: '$21.50',
    target: '$25.50-$26.00',
    rr: '1:2.5+',
    catalyst: 'Citigroup raised PT to $28 from $25',
    ideaDate: '',
    enterDate: '',
  },
  {
    symbol: 'HIMS',
    status: 'waiting',
    setupType: 'Upside Continuation',
    rating: '6/10',
    entry: '$50',
    stop: '$44',
    target: '$58',
    rr: '1:1.33',
    ideaDate: '',
    enterDate: '',
  },
  {
    symbol: 'OKLO',
    status: 'waiting',
    setupType: 'Double Top short',
    rating: '6/10',
    entry: 'Close < $47.00 (Vol 3-5M+)',
    stop: '$48.50',
    target: '$38.00',
    rr: '1:6',
    ideaDate: '',
    enterDate: '',
  },
  {
    symbol: 'SOC',
    status: 'closed',
    setupType: 'Breakout',
    rating: '8/10',
    entry: '$24.60',
    stop: '$23.70',
    target: '$26.50',
    rr: '1:3.5',
    pl: '-$4.61',
    exitReason: 'Securities investigation, legal concerns',
    ideaDate: 'June 5',
    enterDate: 'June 6',
  },
  {
    symbol: 'GLXY',
    status: 'waiting',
    setupType: 'Double Top short',
    rating: '8.5/10',
    entry: 'Break < $18.90',
    stop: '$20.50',
    target: '$15.50',
    rr: '1:2.3',
    ideaDate: 'June 7',
    enterDate: '',
  },
  {
    symbol: 'XBI',
    status: 'waiting',
    setupType: 'Breakout',
    rating: '7.5/10',
    entry: 'Break > 84.30',
    stop: '82',
    target: '$87-88 / $90.77',
    rr: '2-3:1',
    ideaDate: 'June 7',
    enterDate: '',
  },
  {
    symbol: 'SOC',
    status: 'closed',
    setupType: 'Breakout',
    rating: '8/10',
    entry: '$24.60',
    stop: '$23.70',
    target: '$26.50',
    rr: '1:3.5',
    positionSize: 40,
    capitalAtRisk: '$40',
    riskPerShare: '$0.50-0.80',
    exit: '$24.51',
    exitAvg: '$24.51',
    pl: -4.61,
    tradingLoss: '-$3.60',
    commission: '-$1.01',
    ideaDate: 'June 5',
    enterDate: 'June 6',
    exitDate: 'June 9',
    exitReason: `Securities investigation announcement by Kirby McInerney LLP regarding potential violations of federal securities laws. Investigation centers on allegedly misleading statements about production restart during $295M public offering in May 2025. California State Land Commission contradicted company's press release, calling it a mischaracterization that caused "significant public confusion." Court injunction followed, stock dropped 15% on May 28.`,
  },
  {
    symbol: 'INTER',
    status: 'closed',
    setupType: 'Oversold Bounce (Bullish Engulfing @ Support)',
    rating: '7.5/10',
    entry: '$6.75',
    stop: '$6.68',
    target: '$6.91 (MA20 zone), $6.99 (MA50 zone)',
    rr: '1:2.3 to 1:3.4',
    positionSize: 100,
    capitalAtRisk: '$7',
    riskPerShare: '$0.07',
    exitAvg: '$6.95',
    commission: '-$2.01',
    ideaDate: 'June 9',
    enterDate: 'June 9',
    exitDate: 'June 11',
    pl: ((6.95 - 6.75) * 100 - 2.01).toFixed(2), // $18.99
  },
  {
    symbol: 'ACHR',
    status: 'closed',
    setupType: 'Breakout Retest + Momentum Continuation',
    rating: '9/10',
    entry: '$11.24',
    stop: '$10.80',
    target: '$12.50',
    rr: '1:2.9',
    positionSize: 85,
    riskPerShare: '$0.44',
    exitAvg: '$12.17',
    commission: '-$4.02',
    ideaDate: 'June 5, 2025',
    enterDate: 'June 9, 2025',
    exitDate: 'June 11, 2025',
    pl: ((12.17 - 11.24) * 85 - 4.02).toFixed(2), // $74.19
    catalyst: 'Executive Order support + eVTOL momentum + 2028 Olympics contract',
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
        Swing Trading Journal
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
            <p><span class="font-semibold">Entry:</span> {{ trade.entry }}</p>
            <p><span class="font-semibold">Stop:</span> {{ trade.stop }}</p>
            <p><span class="font-semibold">Target:</span> {{ trade.target }}</p>
            <p><span class="font-semibold">Risk/Reward:</span> {{ trade.rr }}</p>
            <p><span class="font-semibold">Rating:</span> {{ trade.rating }}</p>
            <p v-if="trade.catalyst" class="col-span-2">
              <span class="font-semibold">Catalyst:</span> {{ trade.catalyst }}
            </p>
          </div>

          <div
            v-if="trade.status === 'closed'"
            class="mt-2 text-sm font-bold"
            :class="{ 'text-green-600': plNumber(trade) > 0, 'text-red-600': plNumber(trade) < 0 }"
          >
            <p>
              P/L: <span class="font-mono">{{ plNumber(trade) }}</span>
            </p>
            <p class="font-normal text-gray-500">Exit Reason: {{ trade.exitReason }}</p>
          </div>

          <div class="mt-3 flex justify-between text-xs text-gray-500">
            <span>💡 {{ trade.ideaDate }}</span>
            <span v-if="trade.enterDate">🏁 {{ trade.enterDate }}</span>
          </div>

          <button
            class="absolute top-3 right-4 text-gray-400 hover:text-blue-600 transition-colors text-xl opacity-0 group-hover:opacity-100"
            title="More actions"
          >
            ⋮
          </button>
        </CardContent>
      </Card>
    </div>
  </div>
</template>
