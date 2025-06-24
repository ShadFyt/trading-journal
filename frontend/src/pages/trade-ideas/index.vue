<script setup lang="ts">
import { TradeIdeaCardView } from '@/components/trade-ideas'
import { Button } from '@/components/ui/button'
import { Plus } from 'lucide-vue-next'
import { ref } from 'vue'
import SlideOverPanel from '@/components/ui/SlideOverPanel.vue'

const isPanelOpen = ref(false)

function openPanel() {
  isPanelOpen.value = true
}

function closePanel() {
  isPanelOpen.value = false
}
</script>

<template>
  <div class="flex flex-col h-full">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold">Trade Ideas</h1>
      <Button @click="openPanel">
        <Plus class="w-4 h-4 mr-2" />
        Add Trade Idea
      </Button>
    </div>

    <!-- Trade Ideas List -->
    <div class="flex-1 overflow-y-auto">
      <TradeIdeaCardView />
    </div>

    <!-- Slide Over Panel for adding new trade ideas -->
    <SlideOverPanel v-model:is-open="isPanelOpen" title="Add New Trade Idea">
      <div class="space-y-4">
        <div>
          <label for="symbol" class="block text-sm font-medium text-gray-700">Symbol</label>
          <input
            type="text"
            id="symbol"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            placeholder="e.g. AAPL"
          />
        </div>
        <div>
          <label for="entry-price" class="block text-sm font-medium text-gray-700">
            Entry Price
          </label>
          <input
            type="number"
            id="entry-price"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            placeholder="e.g. 150.50"
            step="0.01"
          />
        </div>
        <div>
          <label for="target-price" class="block text-sm font-medium text-gray-700">
            Target Price
          </label>
          <input
            type="number"
            id="target-price"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            placeholder="e.g. 165.00"
            step="0.01"
          />
        </div>
        <div>
          <label for="notes" class="block text-sm font-medium text-gray-700">Notes</label>
          <textarea
            id="notes"
            rows="3"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            placeholder="Add any additional notes or analysis..."
          ></textarea>
        </div>
      </div>

      <template #footer>
        <div class="flex justify-end space-x-3">
          <Button variant="outline" @click="closePanel">Cancel</Button>
          <Button>Save</Button>
        </div>
      </template>
    </SlideOverPanel>
  </div>
</template>
