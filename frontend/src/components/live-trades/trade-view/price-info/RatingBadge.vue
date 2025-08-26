<script setup lang="ts">
const { rating } = defineProps<{ rating: number }>()

const RATING_CLASSES = [
  [2, 'bg-red-100 text-red-800'],
  [4, 'bg-orange-100 text-orange-800'],
  [6, 'bg-yellow-100 text-yellow-800'],
  [8, 'bg-green-100 text-green-800'],
  [Infinity, 'bg-emerald-100 text-emerald-800'],
] as const

const ratingBadgeClass = computed(() => {
  const val = Number(rating ?? 0)
  if (!Number.isFinite(val)) return 'bg-gray-100 text-gray-800' // fallback
  const r = Math.min(10, Math.max(0, val))
  return RATING_CLASSES.find(([max]) => r <= max)![1]
})
</script>

<template>
  <span
    class="inline-flex items-center rounded-full px-2 py-0.5 text-sm font-medium align-middle"
    :class="ratingBadgeClass"
    :aria-label="`Trade quality rating ${rating}/10`"
  >
    {{ rating }}/10
  </span>
</template>
