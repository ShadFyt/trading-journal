<script setup lang="ts">
import type { ScalePlan } from '@/interfaces'

const { executions } = defineProps<{
  executions: ScalePlan['executions']
  open: boolean
}>()

const emit = defineEmits<{
  'update:selected': [ids: string[]]
}>()

const selectedExecutions = ref<string[]>(executions.map((exec) => exec.id))

const toggleExecution = (executionId: string) => {
  const index = selectedExecutions.value.indexOf(executionId)
  if (index > -1) {
    selectedExecutions.value.splice(index, 1)
  } else {
    selectedExecutions.value.push(executionId)
  }
  emit('update:selected', selectedExecutions.value)
}

const toggleSelectAll = () => {
  const allSelected = selectedExecutions.value.length === executions.length
  selectedExecutions.value = allSelected ? [] : executions.map((exec) => exec.id)
  emit('update:selected', selectedExecutions.value)
}

const hasSelection = computed(() => selectedExecutions.value.length > 0)
</script>

<template>
  <div class="space-y-4">
    <div class="flex items-center justify-between">
      <p class="text-sm text-muted-foreground">Select executions to delete:</p>
      <Button variant="ghost" size="sm" @click="toggleSelectAll" class="h-auto p-1 text-xs">
        {{ selectedExecutions.length === executions.length ? 'Deselect All' : 'Select All' }}
      </Button>
    </div>
    <div class="space-y-2 max-h-48 overflow-y-auto">
      <div
        v-for="execution in executions"
        :key="execution.id"
        class="flex items-center space-x-3 cursor-pointer p-2 rounded-md hover:bg-muted/50 transition-colors"
      >
        <Checkbox
          :id="execution.id"
          :model-value="selectedExecutions.includes(execution.id)"
          @update:model-value="() => toggleExecution(execution.id)"
        />
        <label
          :for="execution.id"
          class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
        >
          <span class="font-medium">{{ execution.qty }} shares</span>
          <span class="text-muted-foreground"> @ ${{ execution.price }}</span>
        </label>
      </div>
    </div>
    <div v-if="!hasSelection" class="text-xs text-destructive">
      At least one execution must be selected
    </div>
  </div>
</template>
