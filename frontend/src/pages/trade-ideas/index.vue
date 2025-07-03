<script setup lang="ts">
import { TradeIdeaCardView } from '@/components/trade-ideas'
import { Button } from '@/components/ui/button'
import { Plus } from 'lucide-vue-next'
import { ref } from 'vue'
import SlideOverPanel from '@/components/ui/SlideOverPanel.vue'
import TradeIdeaForm from '@/components/trade-ideas/TradeIdeaForm.vue'

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
      <TradeIdeaForm />

      <template #footer>
        <div class="flex justify-end space-x-3">
          <Button variant="outline" @click="closePanel">Cancel</Button>
          <Button>Save</Button>
        </div>
      </template>
    </SlideOverPanel>
  </div>
</template>
