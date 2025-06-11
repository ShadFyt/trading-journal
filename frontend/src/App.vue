<template>
  <div class="p-4 max-w-7xl mx-auto">
    <div class="flex justify-between items-center mb-4">
      <h1 class="text-2xl font-bold">Swing Trading Journal</h1>
      <Select v-model="filter" class="w-48">
        <SelectTrigger>
          <SelectValue placeholder="Filter by Status" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">All</SelectItem>
          <SelectItem value="active">Active</SelectItem>
          <SelectItem value="closed">Closed</SelectItem>
          <SelectItem value="waiting">Watchlist</SelectItem>
        </SelectContent>
      </Select>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <Card v-for="trade in filteredTrades" :key="trade.symbol">
        <CardContent>
          <div class="flex justify-between items-center">
            <h2 class="text-xl font-semibold">{{ trade.symbol }}</h2>
            <Badge :variant="badgeVariant(trade.status)">{{ trade.status }}</Badge>
          </div>
          <p class="text-sm text-gray-500">{{ trade.setupType }}</p>

          <div class="mt-2 text-sm space-y-1">
            <p><span class="font-semibold">Entry:</span> {{ trade.entry }}</p>
            <p><span class="font-semibold">Stop:</span> {{ trade.stop }}</p>
            <p><span class="font-semibold">Target:</span> {{ trade.target }}</p>
            <p><span class="font-semibold">Risk/Reward:</span> {{ trade.rr }}</p>
            <p><span class="font-semibold">Rating:</span> {{ trade.rating }}</p>
            <p v-if="trade.catalyst"><span class="font-semibold">Catalyst:</span> {{ trade.catalyst }}</p>
          </div>

          <div v-if="trade.status === 'closed'" class="mt-2 text-sm text-red-600">
            <p><span class="font-semibold">P/L:</span> {{ trade.pl }}</p>
            <p><span class="font-semibold">Exit Reason:</span> {{ trade.exitReason }}</p>
          </div>

          <div class="mt-3 flex justify-between text-xs text-gray-400">
            <p>Idea Date: {{ trade.ideaDate }}</p>
            <p v-if="trade.enterDate">Entered: {{ trade.enterDate }}</p>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Card, CardContent } from '@/components/ui/card'
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from '@/components/ui/select'
import { Badge } from '@/components/ui/badge'

const filter = ref('all')

const trades = ref([
  {
    symbol: 'CCL', status: 'waiting', setupType: 'Ascending Triangle Breakout + Golden Cross Formation', rating: '80/10',
    entry: '$22.50-$23.00', stop: '$21.50', target: '$25.50-$26.00', rr: '1:2.5+',
    catalyst: 'Citigroup raised PT to $28 from $25', ideaDate: '', enterDate: ''
  },
  {
    symbol: 'HIMS', status: 'waiting', setupType: 'Upside Continuation', rating: '6/10',
    entry: '$50', stop: '$44', target: '$58', rr: '1:1.33', ideaDate: '', enterDate: ''
  },
  {
    symbol: 'OKLO', status: 'waiting', setupType: 'Double Top short', rating: '6/10',
    entry: 'Close < $47.00 (Vol 3-5M+)', stop: '$48.50', target: '$38.00', rr: '1:6', ideaDate: '', enterDate: ''
  },
  {
    symbol: 'SOC', status: 'closed', setupType: 'Breakout', rating: '8/10',
    entry: '$24.60', stop: '$23.70', target: '$26.50', rr: '1:3.5', pl: '-$4.61',
    exitReason: 'Securities investigation, legal concerns', ideaDate: 'June 5', enterDate: 'June 6'
  },
  {
    symbol: 'GLXY', status: 'waiting', setupType: 'Double Top short', rating: '8.5/10',
    entry: 'Break < $18.90', stop: '$20.50', target: '$15.50', rr: '1:2.3', ideaDate: 'June 7', enterDate: ''
  },
  {
    symbol: 'XBI', status: 'waiting', setupType: 'Breakout', rating: '7.5/10',
    entry: 'Break > 84.30', stop: '82', target: '$87-88 / $90.77', rr: '2-3:1', ideaDate: 'June 7', enterDate: ''
  },
  {
    symbol: 'SOXX', status: 'waiting', setupType: 'Breakout', rating: '8.5/10',
    entry: '$218', stop: '$210', target: '$235-$245', rr: '2.1 to 3.4:1', ideaDate: 'June 7', enterDate: ''
  },
  {
    symbol: 'INTER', status: 'active', setupType: 'Oversold Bounce', rating: '7.5/10',
    entry: '$6.75', stop: '$6.68', target: '$6.91-$6.99', rr: '1:2.3 to 1:3.4', ideaDate: 'June 9', enterDate: 'June 9'
  },
  {
    symbol: 'ACHR', status: 'active', setupType: 'Breakout Retest + Momentum Continuation', rating: '9/10',
    entry: '$11.24', stop: '$10.80', target: '$12.50', rr: '1:2.9',
    catalyst: 'Executive Order + Olympics contract', ideaDate: 'June 5', enterDate: 'June 9'
  }
])

const filteredTrades = computed(() => {
  if (filter.value === 'all') return trades.value
  return trades.value.filter(t => t.status.toLowerCase() === filter.value)
})

const badgeVariant = (status: string) => {
  if (status === 'active') return 'success'
  if (status === 'closed') return 'destructive'
  return 'secondary'
}
</script>

<style scoped>
</style>

