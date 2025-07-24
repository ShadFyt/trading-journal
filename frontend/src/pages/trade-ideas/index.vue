<script setup lang="ts">
import { TradeIdeaCardView, TradeIdeaForm } from '@/components/trade-ideas'
import { ref } from 'vue'

const isFormOpen = ref(false)

const closeForm = () => {
  isFormOpen.value = false
}
</script>

<template>
  <div class="flex flex-col h-full">
    <aside>
      <TradeIdeaForm :isOpen="isFormOpen" :close="closeForm">
        <template #trigger-button>
          <FabRoutingButton
            message="Add Trade Idea"
            iconName="lucide:plus"
            position="bottom-right"
            size="s"
            @click="isFormOpen = true"
          />
        </template>
      </TradeIdeaForm>
    </aside>

    <main class="flex-1 overflow-y-auto">
      <TradeIdeaCardView />
    </main>
  </div>
</template>
