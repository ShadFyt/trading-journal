<script lang="ts" setup>
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'

import { Icon } from '@iconify/vue'

const emit = defineEmits<{
  (e: 'remove-plan'): []
}>()
</script>

<template>
  <PlanFormHeader @remove-plan="emit('remove-plan')" />
  <div class="space-y-4">
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <OrderTypeField />
      <FormField class="space-y-2" name="label" v-slot="{ componentField }">
        <FormItem>
          <FormLabel for="label" class="text-xs font-medium text-slate-300 flex items-center gap-1">
            Label
          </FormLabel>
          <Input
            v-bind="componentField"
            class="w-full bg-slate-800 border border-slate-600 text-slate-200 placeholder:text-slate-400 focus-visible:ring-emerald-500 focus-visible:border-emerald-500"
          />
          <FormMessage class="text-red-500" />
        </FormItem>
      </FormField>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <QtyField />
      <FormField class="space-y-2" name="targetPrice" v-slot="{ componentField }">
        <FormItem>
          <FormLabel
            for="targetPrice"
            class="text-xs font-medium text-slate-300 flex items-center gap-1"
          >
            <Icon icon="lucide:dollar-sign" width="14" height="14" class="text-slate-400" />
            Est. Target Price
          </FormLabel>
          <Input
            type="number"
            v-bind="componentField"
            min="0"
            step="0.01"
            placeholder="0.00"
            class="w-full bg-slate-800 border border-slate-600 text-slate-200 placeholder:text-slate-400 focus-visible:ring-emerald-500 focus-visible:border-emerald-500"
          />
          <FormMessage class="text-red-500" />
        </FormItem>
      </FormField>
    </div>

    <NoteField />
  </div>
</template>
