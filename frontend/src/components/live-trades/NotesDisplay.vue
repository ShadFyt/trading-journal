<script lang="ts" setup>
import type { LiveTrade } from '@/interfaces'

const { trade } = defineProps<{ trade: LiveTrade }>()

// Reactive states for notes display
const showAllCatalysts = ref(false)
const showAllNotes = ref(false)

const displayedCatalysts = computed(() => {
  return showAllCatalysts.value ? trade.catalysts : trade.catalysts.slice(0, 1)
})

const displayedNotes = computed(() => {
  return showAllNotes.value ? trade.notes : trade.notes.slice(0, 1)
})

const formatDate = (date: Date) => {
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}
</script>

<template>
  <section class="space-y-3">
    <div>
      <p class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Setup</p>
      <p class="text-xs text-gray-500 italic">{{ trade.setup }}</p>
    </div>

    <!-- Catalysts -->
    <div v-if="trade.catalysts.length > 0">
      <div class="flex justify-between items-center">
        <p class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Catalysts</p>
        <Button
          v-if="trade.catalysts.length > 1"
          variant="ghost"
          size="sm"
          class="text-xs px-2 py-1 h-auto text-blue-600 hover:text-blue-700"
          @click="showAllCatalysts = !showAllCatalysts"
        >
          {{ showAllCatalysts ? 'Show Less' : `+${trade.catalysts.length - 1} more` }}
        </Button>
      </div>
      <div class="space-y-2">
        <div
          v-for="catalyst in displayedCatalysts"
          :key="catalyst.id"
          class="text-xs text-gray-500 italic border-l-2 border-blue-200 pl-2"
        >
          <div class="flex justify-between items-start">
            <span>{{ catalyst.content }}</span>
            <span class="text-gray-400 text-[10px]">{{ formatDate(catalyst.date) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Notes -->
    <div v-if="trade.notes.length > 0">
      <div class="flex justify-between items-center">
        <p class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Notes</p>
        <Button
          v-if="trade.notes.length > 1"
          variant="ghost"
          size="sm"
          class="text-xs px-2 py-1 h-auto text-blue-600 hover:text-blue-700"
          @click="showAllNotes = !showAllNotes"
        >
          {{ showAllNotes ? 'Show Less' : `+${trade.notes.length - 1} more` }}
        </Button>
      </div>
      <div class="space-y-2">
        <div
          v-for="note in displayedNotes"
          :key="note.id"
          class="text-xs text-gray-500 italic border-l-2 border-green-200 pl-2"
        >
          <div class="flex justify-between items-start">
            <span>{{ note.content }}</span>
            <span class="text-gray-400 text-[10px]">{{ formatDate(note.date) }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
