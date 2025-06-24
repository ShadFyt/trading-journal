<script setup lang="ts">
import { X } from 'lucide-vue-next'
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'

const props = defineProps<{
  isOpen: boolean
  title?: string
  description?: string
}>()

const emit = defineEmits<{
  (e: 'update:isOpen', value: boolean): void
  (e: 'close'): void
}>()

const panel = ref<HTMLElement | null>(null)
const isVisible = ref(false)

function close() {
  emit('update:isOpen', false)
  emit('close')
}

// Handle escape key press
function handleEscapeKey(event: KeyboardEvent) {
  if (event.key === 'Escape' && props.isOpen) {
    close()
  }
}

// Handle click outside
function handleClickOutside(event: MouseEvent) {
  if (panel.value && !panel.value.contains(event.target as Node) && props.isOpen) {
    close()
  }
}

// Watch for isOpen changes to control animation
watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal) {
      // Small delay to ensure CSS transition works properly
      setTimeout(() => {
        isVisible.value = true
        document.body.classList.add('overflow-hidden')
      }, 10)
    } else {
      isVisible.value = false
      document.body.classList.remove('overflow-hidden')
    }
  },
)

onMounted(() => {
  document.addEventListener('keydown', handleEscapeKey)
  document.addEventListener('mousedown', handleClickOutside)

  if (props.isOpen) {
    isVisible.value = true
    document.body.classList.add('overflow-hidden')
  }
})

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleEscapeKey)
  document.removeEventListener('mousedown', handleClickOutside)
  document.body.classList.remove('overflow-hidden')
})

defineExpose({
  close,
})
</script>

<template>
  <!-- Backdrop overlay -->
  <Transition name="fade">
    <div
      v-if="props.isOpen"
      class="fixed inset-0 bg-black/30 backdrop-blur-sm z-40"
      aria-hidden="true"
    ></div>
  </Transition>

  <!-- Slide-over panel -->
  <Transition name="slide-over">
    <div
      v-if="props.isOpen"
      ref="panel"
      class="fixed inset-y-0 right-0 z-50 w-full max-w-md overflow-y-auto bg-white shadow-xl"
      :class="{ 'translate-x-0': isVisible, 'translate-x-full': !isVisible }"
      role="dialog"
      aria-modal="true"
      aria-labelledby="slide-over-title"
    >
      <!-- Header with title and close button -->
      <div class="sticky top-0 z-10 border-b border-gray-200 bg-white px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <h2 v-if="title" id="slide-over-title" class="text-lg font-semibold text-gray-900">
              {{ title }}
            </h2>
            <p v-if="description" class="mt-1 text-sm text-gray-500">
              {{ description }}
            </p>
          </div>
          <button
            @click="close"
            class="rounded-md text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500"
            aria-label="Close panel"
          >
            <X class="h-5 w-5" />
          </button>
        </div>
      </div>

      <!-- Panel content -->
      <div class="px-6 py-6">
        <slot></slot>
      </div>

      <!-- Footer -->
      <div v-if="$slots.footer" class="border-t border-gray-200 bg-gray-50 px-6 py-4">
        <slot name="footer"></slot>
      </div>
    </div>
  </Transition>
</template>
