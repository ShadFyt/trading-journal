<script lang="ts" setup>
defineProps<{ extraClasses?: string; title: string }>()
</script>

<template>
  <div class="rounded bg-slate-700 p-2">
    <p class="text-xs text-slate-300">{{ title }}</p>
    <p class="font-medium" :class="extraClasses">
      <slot />
    </p>
  </div>
</template>
