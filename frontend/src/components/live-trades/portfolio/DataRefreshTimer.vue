<script setup lang="ts">
import { Icon } from '@iconify/vue'
import type { RefetchOptions } from '@tanstack/vue-query'

const emit = defineEmits<{
  (e: 'refetch-live-trades', options?: RefetchOptions): void
}>()

let interval: ReturnType<typeof setInterval> | null = null
const refetchProgress = ref(0)

const handleRefresh = () => {
  emit('refetch-live-trades')
  refetchProgress.value = 0
}

const startTimer = () => {
  refetchProgress.value = 0
  interval = setInterval(() => {
    refetchProgress.value += 1.6667
    if (refetchProgress.value >= 100) {
      handleRefresh()
    }
  }, 500)
}

onMounted(() => {
  startTimer()
})

onUnmounted(() => {
  if (interval) {
    clearInterval(interval)
  }
})
</script>
<template>
  <div class="w-1/3">
    <span class="text-sm text-gray-100">Data Refresh Timer</span>
    <div class="flex items-center gap-3">
      <Progress v-model="refetchProgress" class="w-5/5 h-3 bg-gray-900" />
      <Icon
        icon="lucide:refresh-cw"
        width="24"
        height="24"
        @click="handleRefresh"
        class="cursor-pointer hover:opacity-75 text-blue-200"
      />
    </div>
  </div>
</template>
