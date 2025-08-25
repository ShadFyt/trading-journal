<script setup lang="ts">
interface Props {
  title: string
}

defineProps<Props>()
</script>

<template>
  <div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
    <header class="mb-2">
      <h3 class="text-sm font-semibold text-gray-600 uppercase tracking-wide">
        {{ title }}
      </h3>
    </header>
    <div class="text-2xl font-bold">
      <slot />
    </div>
  </div>
</template>
