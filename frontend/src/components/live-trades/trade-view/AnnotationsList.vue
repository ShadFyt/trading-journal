<script lang="ts" setup>
import type { Annotation } from '@/interfaces'
import { Icon } from '@iconify/vue'
import { useAnnotationMutationService, useFormatters } from '@/composables'
import { PopoverContent, PopoverPortal, PopoverRoot, PopoverTrigger } from 'reka-ui'

const props = defineProps<{
  annotations: Annotation[]
  type: 'note' | 'catalyst'
  tradeId: string
  title: string
}>()

const { createMutation } = useAnnotationMutationService()
const newAnnotation = ref('')
const showAll = ref(false)

const filtered = computed(() => props.annotations.filter((a) => a.type === props.type))
const displayed = computed(() => (showAll.value ? filtered.value : filtered.value.slice(0, 1)))

const borderClass = computed(() =>
  props.type === 'catalyst' ? 'border-blue-200' : 'border-green-200',
)

const { convertStringToDate } = useFormatters()
const formatDate = (date: Date | string) =>
  convertStringToDate(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })

const handleAnnotationCreation = (close: () => void) => {
  createMutation.mutate({
    content: newAnnotation.value,
    type: props.type,
    tradeId: props.tradeId,
  })
  close()
}
</script>

<template>
  <div v-if="filtered.length > 0">
    <div class="flex justify-between items-center">
      <div class="flex justify-between w-full mb-1">
        <p class="text-xs font-semibold text-gray-600 uppercase tracking-wide">{{ title }}</p>
        <Button
          v-if="filtered.length > 1"
          variant="ghost"
          size="sm"
          class="text-xs px-2 py-1 h-auto text-blue-600 hover:text-blue-700"
          @click="showAll = !showAll"
        >
          {{ showAll ? 'Show Less' : `+${filtered.length - 1} more` }}
        </Button>
        <PopoverRoot v-slot="{ close }">
          <PopoverTrigger as-child>
            <Icon
              icon="lucide:message-square-plus"
              width="20"
              height="20"
              class="hover:opacity-80 cursor-pointer"
            />
          </PopoverTrigger>
          <PopoverPortal>
            <PopoverContent
              class="rounded-lg p-5 w-[260px] bg-white shadow-sm border will-change-[transform,opacity] data-[state=open]:data-[side=top]:animate-slideDownAndFade data-[state=open]:data-[side=right]:animate-slideLeftAndFade data-[state=open]:data-[side=bottom]:animate-slideUpAndFade data-[state=open]:data-[side=left]:animate-slideRightAndFade"
            >
              <p class="text-xs font-semibold text-gray-600 uppercase tracking-wide">
                Add {{ type }}
              </p>
              <Textarea
                v-model="newAnnotation"
                id="annotation"
                rows="5"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                :placeholder="`Add any additional ${type} or analysis...`"
              />
              <Button
                class="w-full mt-2"
                variant="default"
                @click="handleAnnotationCreation(close)"
              >
                Save
              </Button>
            </PopoverContent>
          </PopoverPortal>
        </PopoverRoot>
      </div>
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
