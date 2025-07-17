<script setup lang="ts">
import { TradeIdeaCardView, TradeIdeaForm } from '@/components/trade-ideas'
</script>

<template>
  <div class="flex flex-col h-full">
    <div>
      <TradeIdeaForm />
    </div>

    <div class="flex-1 overflow-y-auto">
      <TradeIdeaCardView />
    </div>
  </div>
</template>
