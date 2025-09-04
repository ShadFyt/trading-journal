<script lang="ts" setup>
import type { LiveTrade } from '@/interfaces'
import { useFormatters } from '@/composables'
const { convertStringToDate } = useFormatters()

defineProps<{
  trade: LiveTrade
  isExpanded: boolean
  detailsId: string
}>()

const emit = defineEmits(['toggle'])
</script>

<template>
  <footer
    class="mt-3 pt-2 border-t border-gray-100 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between flex-wrap text-xs text-gray-400"
  >
    <span v-if="trade.enterDate"
      >Entered {{ convertStringToDate(trade.enterDate).toLocaleDateString() }}</span
    >
    <button
      type="button"
      :aria-expanded="isExpanded"
      :aria-controls="detailsId"
      @click="emit('toggle')"
      class="text-blue-600 inline-flex items-center h-11 px-3 min-w-[44px] rounded-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2"
    >
      {{ isExpanded ? 'Collapse' : 'Expand' }}
    </button>
    <span>ID: {{ trade.id.slice(-6) }}</span>
  </footer>
</template>
