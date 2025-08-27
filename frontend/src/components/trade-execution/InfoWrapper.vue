<script lang="ts" setup>
defineProps<{ extraClasses?: string; title: string }>()
</script>

<template>
  <div class="rounded bg-gray-50 p-2">
    <p class="text-xs text-gray-600">{{ title }}</p>
    <p class="font-medium" :class="extraClasses">
      <slot />
    </p>
  </div>
</template>
