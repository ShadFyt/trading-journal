<script lang="ts" setup>
import type { ScalePlan } from '@/interfaces'

const { scalePlan } = defineProps<{ scalePlan: ScalePlan }>()
</script>

<template>
  <p class="text-xs font-semibold text-center mb-3">Execute scale plan {{ scalePlan.label }}</p>
</template>
