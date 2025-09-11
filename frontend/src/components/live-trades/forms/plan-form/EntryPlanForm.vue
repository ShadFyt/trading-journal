<script lang="ts" setup>
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'

import { Icon } from '@iconify/vue'

const { idx } = defineProps<{ idx: string | number }>()
const planId = computed(() => `scalePlans.${idx}`)
</script>

<template>
  <div class="space-y-4">
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <OrderTypeField :plan-id="planId" />
      <TradeTypeField :plan-id="planId" />
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
      <FormField class="space-y-2" :name="`${planId}.limitPrice`" v-slot="{ value, setValue }">
        <FormItem>
          <FormLabel
            :for="`${planId}.limitPrice`"
            class="text-xs font-medium text-slate-300 flex items-center gap-1"
          >
            <Icon icon="lucide:dollar-sign" width="14" height="14" class="text-slate-400" />
            Est. Entry Price
          </FormLabel>
          <Input
            type="number"
            :model-value="value"
            @update:model-value="setValue"
            min="0"
            step="0.01"
            placeholder="0.00"
            class="bg-slate-800 border border-slate-600 text-slate-200 placeholder:text-slate-400"
          />
          <FormMessage class="text-red-500" />
        </FormItem>
      </FormField>
      <FormField class="space-y-2" :name="`${planId}.stopPrice`" v-slot="{ value, setValue }">
        <FormItem>
          <FormLabel
            :for="`${planId}.stopPrice`"
            class="text-xs font-medium text-slate-300 flex items-center gap-1"
          >
            <Icon icon="lucide:dollar-sign" width="14" height="14" class="text-slate-400" />
            Est. Stop Loss
          </FormLabel>
          <Input
            type="number"
            :model-value="value"
            @update:model-value="setValue"
            min="0"
            step="0.01"
            placeholder="0.00"
            class="bg-slate-800 border border-slate-600 text-slate-200 placeholder:text-slate-400"
          />
          <FormMessage class="text-red-500" />
        </FormItem>
      </FormField>
      <QtyField :plan-id="planId" />
    </div>

    <NoteField :plan-id="planId" />
  </div>
</template>
