<script lang="ts" setup>
import type { Trade } from '@/interfaces'
import AnnotationsList from './AnnotationsList.vue'

const { trade } = defineProps<{ trade: Trade }>()
</script>

<template>
  <section class="mt-2">
    <div>
      <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide">Setup</p>
      <p class="text-xs text-gray-100 italic">{{ trade.setup }}</p>
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
