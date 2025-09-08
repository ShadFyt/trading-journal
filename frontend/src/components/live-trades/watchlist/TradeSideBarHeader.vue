<script lang="ts" setup>
import { Icon } from '@iconify/vue'
const emit = defineEmits<{
  (e: 'open-trade-form'): []
}>()
</script>

<template>
  <header class="p-4 border-b border-gray-800">
    <h2 class="text-lg font-semibold text-white mb-2">Watchlist</h2>
    <div class="flex justify-between gap-2 w-full">
      <div class="relative w-full">
        <Input
          placeholder="Search symbols..."
          class="pl-10 bg-gray-800 border-gray-700 text-white placeholder-gray-400"
        />
      </div>
      <Button
        variant="outline"
        size="icon"
        class="text-gray-500 hover:text-gray-400"
        @click="emit('open-trade-form')"
      >
        <Icon icon="lucide:diff" width="24" height="24" />
      </Button>
    </div>
  </header>
</template>
