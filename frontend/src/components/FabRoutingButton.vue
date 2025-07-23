<script setup lang="ts">
/**
 * A floating action button with tooltip and optional routing capabilities.
 *
 * @example
 * // As a FAB with routing:
 * <FabRoutingButton
 *   to="/new-entry"
 *   message="Create new entry"
 *   iconName="plus"
 *   position="bottom-right"
 *   size="m"
 * />
 *
 * // As a regular button with click handler:
 * <FabRoutingButton
 *   message="Open form"
 *   iconName="plus"
 *   @click="handleClick"
 * />
 */
import { useRouter, type RouteLocationRaw } from 'vue-router'
import { Icon } from '@iconify/vue'
import { cn } from '@/lib/utils'
import { ref, computed } from 'vue'
import { Button } from '@/components/ui/button'

const props = withDefaults(
  defineProps<{
    to?: RouteLocationRaw
    message?: string
    iconName?: string
    size?: 's' | 'm' | 'l' | 'xl'
    position?: 'top-left' | 'top-right' | 'bottom-left' | 'bottom-right'
  }>(),
  {
    position: 'bottom-right',
    size: 'm',
    message: '',
  },
)

const emit = defineEmits<{
  (e: 'click', event: MouseEvent): void
}>()
const router = useRouter()
const showTooltip = ref(false)

const sizeClasses = {
  s: 'w-12 h-12',
  m: 'w-14 h-14',
  l: 'w-16 h-16',
  xl: 'w-20 h-20',
} as const

const buttonClasses = computed(() =>
  cn('rounded-full text-white shadow-lg hover:bg-primary/90 transition', sizeClasses[props.size]),
)

const positionClasses = computed(
  () =>
    (
      ({
        'top-left': 'top-6 left-6',
        'top-right': 'top-6 right-6',
        'bottom-left': 'bottom-6 left-6',
        'bottom-right': 'bottom-6 right-6',
      }) as const
    )[props.position] || 'bottom-right',
)

const handleClick = (event: MouseEvent) => {
  if (props.to) {
    router.push(props.to)
  }
  emit('click', event)
}
</script>

<template>
  <div :class="['fixed', positionClasses]" class="z-50">
    <div class="relative">
      <transition name="fade">
        <div
          v-if="showTooltip && message"
          class="absolute px-3 py-2 rounded-lg bg-gray-900 text-white text-sm shadow-lg whitespace-nowrap"
          :class="positionClasses.includes('right-') ? 'right-full mr-2' : 'left-full ml-2'"
          style="pointer-events: none"
        >
          {{ message }}
        </div>
      </transition>
      <Button
        @mouseenter="showTooltip = true"
        @mouseleave="showTooltip = false"
        @focus="showTooltip = true"
        @blur="showTooltip = false"
        @click="handleClick"
        :class="buttonClasses"
        :aria-label="message || 'Button'"
        data-testid="fab-button"
      >
        <slot name="icon">
          <Icon :icon="iconName || 'lucide:plus'" class="text-2xl" />
        </slot>
        <slot>
          <span v-if="!iconName">{{ message }}</span>
        </slot>
      </Button>
    </div>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
