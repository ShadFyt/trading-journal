<script lang="ts" setup>
const props = withDefaults(
  defineProps<{
    modelValue?: number
    rating?: number
    max?: number
    step?: number
    readOnly?: boolean
    displayText?: boolean
    size?: 'sm' | 'md' | 'lg'
    label?: string
    showMaxValue?: boolean
  }>(),
  {
    max: 10,
    step: 0.1,
    readOnly: false,
    size: 'sm',
    label: 'Rating',
    displayText: true,
    showMaxValue: true,
  },
)

const internal = ref<number>(props.modelValue ?? props.rating ?? 0)
const valueToUse = computed(() => internal.value)

const getBadgeClasses = (rating: number) => {
  if (rating >= 8.0) {
    return 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
  } else if (rating >= 6.5) {
    return 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
  } else if (rating >= 5.0) {
    return 'bg-orange-500/20 text-orange-300 border border-orange-500/30'
  } else {
    return 'bg-red-500/20 text-red-300 border border-red-500/30'
  }
}

// Size variants for the badge
const getSizeClasses = (size: string) => {
  switch (size) {
    case 'sm':
      return 'px-2 py-0.5 text-xs'
    case 'lg':
      return 'px-4 py-2 text-base'
    default:
      return 'px-3 py-1 text-sm'
  }
}

const getRatingDescription = (rating: number) => {
  if (rating >= 8.0) return 'Excellent'
  if (rating >= 6.5) return 'Good'
  if (rating >= 5.0) return 'Fair'
  return 'Poor'
}
</script>

<template>
  <div class="inline-flex items-center gap-2 select-none" :aria-label="label">
    <div
      class="inline-flex items-center gap-2 rounded-md font-semibold"
      :class="[getBadgeClasses(valueToUse), getSizeClasses(size)]"
      :title="`${getRatingDescription(valueToUse)} rating: ${valueToUse.toFixed(1)}/${max}`"
      role="img"
      :aria-label="`Rating ${valueToUse.toFixed(1)} out of ${max}, ${getRatingDescription(valueToUse)}`"
    >
      <span>{{ valueToUse.toFixed(1) }}</span>
      <span v-if="showMaxValue && displayText" class="opacity-60 font-normal"> /{{ max }} </span>
    </div>
  </div>
</template>
