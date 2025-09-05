<script lang="ts" setup>
const props = withDefaults(
  defineProps<{
    modelValue?: number
    rating?: number
    max?: number
    step?: number
    readOnly?: boolean
    displayText?: boolean
    showEmpty?: boolean
    size?: 'sm' | 'md' | 'lg'
    filledClass?: string
    emptyClass?: string
    label?: string
  }>(),
  {
    max: 10,
    step: 0.1,
    readOnly: false,
    size: 'md',
    filledClass: 'text-yellow-400',
    emptyClass: 'text-slate-300',
    label: 'Star rating',
    displayText: true,
    showEmpty: false,
  },
)

const internal = ref<number>(props.modelValue ?? props.rating ?? 0)
const hovering = ref<boolean>(false)
const hoverValue = ref<number>(internal.value)

const valueToUse = computed(() => (hovering.value ? hoverValue.value : internal.value))
const starCount = computed(() => {
  if (props.showEmpty) return props.max
  return Math.min(Math.max(Math.ceil(props.rating ?? 0), 0), props.max)
})

const sizePx = computed(
  () =>
    ({
      sm: 16,
      md: 22,
      lg: 28,
    })[props.size],
)

const clamp = (n: number, min: number, max: number) => Math.min(Math.max(n, min), max)

const starFillPercent = (starIndex: number) => {
  // starIndex is 0-based; compute how much of this star is filled in %
  const v = valueToUse.value
  const diff = v - starIndex
  if (diff >= 1) return 100
  if (diff <= 0) return 0
  return clamp(diff * 100, 0, 100)
}
</script>

<template>
  <div class="inline-flex items-center gap-2 select-none" :aria-label="label">
    <div
      class="group relative inline-flex items-center outline-none"
      role="slider"
      :aria-valuemin="0"
      :aria-valuemax="starCount"
      :aria-valuenow="Number(internal.toFixed(2))"
      :tabindex="readOnly ? -1 : 0"
    >
      <template v-for="i in starCount" :key="i">
        <button
          type="button"
          class="relative p-0 m-0 appearance-none bg-transparent border-0 cursor-pointer"
          :class="readOnly ? 'cursor-default' : 'cursor-pointer'"
          :style="{ width: sizePx + 'px', height: sizePx + 'px' }"
          :disabled="readOnly"
        >
          <!-- Empty Star -->
          <svg
            :width="sizePx"
            :height="sizePx"
            viewBox="0 0 24 24"
            class="block"
            :class="emptyClass"
            aria-hidden="true"
            v-if="showEmpty"
          >
            <path
              fill="currentColor"
              d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
            />
          </svg>

          <div
            class="absolute inset-0 overflow-hidden"
            :style="{ width: starFillPercent(i - 1) + '%' }"
          >
            <svg
              :width="sizePx"
              :height="sizePx"
              viewBox="0 0 24 24"
              class="block"
              :class="filledClass"
              aria-hidden="true"
            >
              <path
                fill="currentColor"
                d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"
              />
            </svg>
          </div>
        </button>
      </template>
    </div>

    <span v-if="displayText" class="text-xs font-medium text-slate-600" :aria-hidden="true">
      {{ valueToUse.toFixed(1) }} / {{ max }}
    </span>
  </div>
</template>
