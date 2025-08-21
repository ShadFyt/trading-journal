<script lang="ts" setup>
defineProps<{
  isSubmitting: boolean
}>()
</script>

<template>
  <!-- Loading spinner -->
  <div v-if="isSubmitting" class="absolute inset-0 flex items-center justify-center z-50">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
  </div>
</template>
