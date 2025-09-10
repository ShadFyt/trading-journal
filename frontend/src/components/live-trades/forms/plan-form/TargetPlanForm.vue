<script lang="ts" setup>
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'

import { Icon } from '@iconify/vue'
import type { ScalePlanCreate } from '@/interfaces'
const { idx } = defineProps<{ idx: string | number }>()
const planId = computed(() => `scalePlans.${idx}`)

const plan = defineModel<ScalePlanCreate>()

const emit = defineEmits<{
  (e: 'remove-plan'): []
}>()
</script>

<template>
  <PlanFormHeader @remove-plan="emit('remove-plan')" />
  <div class="space-y-4" v-if="plan">
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <OrderTypeField :plan-id="planId" />
      <FormField class="space-y-2" :name="`${planId}.label`" v-slot="{ value, setValue }">
        <FormItem>
          <FormLabel
            :for="`${planId}.label`"
            class="text-xs font-medium text-slate-300 flex items-center gap-1"
          >
            Label
          </FormLabel>
          <Input
            :model-value="value"
            @update:model-value="setValue"
            class="w-full bg-slate-800 border border-slate-600 text-slate-200 placeholder:text-slate-400 focus-visible:ring-emerald-500 focus-visible:border-emerald-500"
          />
          <FormMessage class="text-red-500" />
        </FormItem>
      </FormField>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <QtyField :plan-id="planId" />
      <FormField class="space-y-2" :name="`${planId}.targetPrice`" v-slot="{ value, setValue }">
        <FormItem>
          <FormLabel
            :for="`${planId}.targetPrice`"
            class="text-xs font-medium text-slate-300 flex items-center gap-1"
          >
            <Icon icon="lucide:dollar-sign" width="14" height="14" class="text-slate-400" />
            Est. Target Price
          </FormLabel>
          <Input
            type="number"
            :model-value="value"
            @update:model-value="setValue"
            min="0"
            step="0.01"
            placeholder="0.00"
            class="w-full bg-slate-800 border border-slate-600 text-slate-200 placeholder:text-slate-400 focus-visible:ring-emerald-500 focus-visible:border-emerald-500"
          />
          <FormMessage class="text-red-500" />
        </FormItem>
      </FormField>
    </div>

    <NoteField :plan-id="planId" />
  </div>
</template>
