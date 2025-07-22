<script setup lang="ts">
import { TradeIdeaCardView, TradeIdeaForm } from '@/components/trade-ideas'
</script>

<template>
  <div class="flex flex-col h-full">
    <aside>
      <TradeIdeaForm>
        <template #trigger-button>
          <FabRoutingButton
            message="Add Trade Idea"
            iconName="lucide:plus"
            position="bottom-right"
            size="s"
          />
        </template>
      </TradeIdeaForm>
    </aside>

    <main class="flex-1 overflow-y-auto">
      <TradeIdeaCardView />
    </main>
  </div>
</template>
