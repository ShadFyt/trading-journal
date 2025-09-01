<script lang="ts" setup>
defineProps<{ isGreen: boolean; title: string }>()
</script>

<template>
  <div class="flex sm:flex-col justify-between sm:justify-between sm:h-full">
    <p class="text-xs text-gray-600 uppercase tracking-wide">{{ title }}</p>
    <span
      class="text-base font-bold sm:mt-1 sm:text-xl"
      :class="isGreen ? 'text-emerald-700' : 'text-rose-700'"
      aria-live="polite"
      aria-atomic="true"
    >
      <slot />
    </span>
  </div>
</template>
