<script lang="ts" setup>
import type { LiveTrade } from '@/interfaces'
import AnnotationsList from './AnnotationsList.vue'

const { trade } = defineProps<{ trade: LiveTrade }>()
</script>

<template>
  <section class="space-y-3">
    <div>
      <p class="text-xs font-semibold text-gray-600 uppercase tracking-wide">Setup</p>
      <p class="text-xs text-gray-500 italic">{{ trade.setup }}</p>
    </div>

    <!-- Catalysts -->
    <AnnotationsList
      :annotations="trade.annotations"
      type="catalyst"
      title="Catalysts"
      :tradeId="trade.id"
    />

    <!-- Notes -->
    <AnnotationsList
      :annotations="trade.annotations"
      type="note"
      title="Notes"
      :tradeId="trade.id"
    />
  </section>
</template>
