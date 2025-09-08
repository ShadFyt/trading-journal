<script lang="ts" setup>
import { Icon } from '@iconify/vue'

defineProps<{ isEntry: boolean }>()
const emit = defineEmits<{ remove: [] }>()
</script>

<template>
  <header class="flex items-center bg-blue-700 justify-between mb-4">
    <div class="flex items-center gap-2">
      <Icon icon="lucide:target" width="24" height="24" />
      <span class="font-medium text-md">Target Plans</span>
    </div>
    <Button
      @click="emit('remove')"
      class="text-red-400 hover:text-red-300 p-1 rounded transition-colors"
    >
      <Icon icon="lucide:x" width="24" height="24" />
    </Button>
  </header>
</template>
