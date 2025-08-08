<script lang="ts" setup>
import type { Annotation } from '@/interfaces'
import { Icon } from '@iconify/vue'
import { useFormatters } from '@/composables'

const props = defineProps<{
  annotations: Annotation[]
  type: 'note' | 'catalyst'
  title: string
}>()

const emit = defineEmits<{
  (e: 'add', type: 'note' | 'catalyst'): void
}>()

const showAll = ref(false)

const filtered = computed(() => props.annotations.filter((a) => a.type === props.type))
const displayed = computed(() => (showAll.value ? filtered.value : filtered.value.slice(0, 1)))

const borderClass = computed(() =>
  props.type === 'catalyst' ? 'border-blue-200' : 'border-green-200',
)

const { convertStringToDate } = useFormatters()
const formatDate = (date: Date | string) =>
  convertStringToDate(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
</script>

<template>
  <div v-if="filtered.length > 0">
    <div class="flex justify-between items-center">
      <div class="flex justify-between w-full mb-1">
        <p class="text-xs font-semibold text-gray-600 uppercase tracking-wide">{{ title }}</p>
        <Icon
          icon="lucide:message-square-plus"
          width="20"
          height="20"
          class="hover:opacity-80 cursor-pointer"
          @click="emit('add', props.type)"
        />
      </div>
      <Button
        v-if="filtered.length > 1"
        variant="ghost"
        size="sm"
        class="text-xs px-2 py-1 h-auto text-blue-600 hover:text-blue-700"
        @click="showAll = !showAll"
      >
        {{ showAll ? 'Show Less' : `+${filtered.length - 1} more` }}
      </Button>
    </div>

    <div class="space-y-2">
      <div
        v-for="item in displayed"
        :key="item.id"
        class="text-xs text-gray-500 italic pl-2"
        :class="borderClass + ' border-l-2'"
      >
        <div class="flex justify-between items-start">
          <span>{{ item.content }}</span>
          <span class="text-gray-400 text-[10px]">{{ formatDate(item.date) }}</span>
        </div>
      </div>
    </div>
  </div>
</template>
