<script lang="ts" setup>
import { Icon } from '@iconify/vue'

defineProps<{ isEntry: boolean }>()
const emit = defineEmits<{ (e: 'remove-plan'): [] }>()
</script>

<template>
  <header class="flex items-center justify-between mb-4">
    <div class="flex items-center gap-2">
      <Icon icon="lucide:target" width="24" height="24" />
      <span class="font-medium text-md">Target Plans</span>
    </div>
    <Button
      @click.prevent="emit('remove-plan')"
      class="text-red-400 bg-slate-900 hover:text-red-300 rounded transition-colors"
    >
      <Icon icon="lucide:x" />
    </Button>
  </header>
</template>
