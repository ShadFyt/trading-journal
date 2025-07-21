<script setup lang="ts">
import { TradeIdeaCardView, TradeIdeaForm } from '@/components/trade-ideas'
</script>

<template>
  <div class="flex flex-col h-full">
    <aside>
      <TradeIdeaForm />
    </aside>

    <main class="flex-1 overflow-y-auto">
      <TradeIdeaCardView />
    </main>
  </div>
</template>
