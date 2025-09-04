<script setup lang="ts">
interface Props {
  title: string
}

defineProps<Props>()
</script>

<template>
  <div class="bg-slate-800 p-4 rounded-lg border border-gray-200 shadow-sm">
    <header class="mb-2">
      <h3 class="text-sm font-semibold text-slate-100 uppercase tracking-wide">
        {{ title }}
      </h3>
    </header>
    <div class="text-2xl font-bold">
      <slot />
    </div>
  </div>
</template>
