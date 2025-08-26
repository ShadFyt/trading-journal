<script lang="ts" setup>
withDefaults(
  defineProps<{
    label: string
    labelClass?: string
    valueClass?: string
  }>(),
  {
    labelClass: 'font-semibold text-gray-600',
    valueClass: 'ml-1',
  },
)
</script>

<template>
  <dt :class="labelClass">{{ label }}</dt>
  <dd :class="valueClass">
    <slot />
  </dd>
</template>
