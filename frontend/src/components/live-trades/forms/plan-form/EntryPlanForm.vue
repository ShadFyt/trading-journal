<script lang="ts" setup>
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
const plan = defineModel<ScalePlanCreate>()

import { Icon } from '@iconify/vue'
import type { ScalePlanCreate } from '@/interfaces'
</script>

<template>
  <div v-if="plan" class="space-y-4">
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <OrderTypeField v-model="plan.orderType" />
      <TradeTypeField />
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
      <FormField class="space-y-2" name="limitPrice" v-slot="{ componentField }">
        <FormItem>
          <FormLabel
            for="limitPrice"
            class="text-xs font-medium text-slate-300 flex items-center gap-1"
          >
            <Icon icon="lucide:dollar-sign" width="14" height="14" class="text-slate-400" />
            Est. Entry Price
          </FormLabel>
          <Input
            type="number"
            v-bind="componentField"
            min="0"
            step="0.01"
            placeholder="0.00"
            class="bg-slate-800 border border-slate-600 text-slate-200 placeholder:text-slate-400 focus-visible:ring-emerald-500 focus-visible:border-emerald-500"
          />
          <FormMessage class="text-red-500" />
        </FormItem>
      </FormField>
      <FormField class="space-y-2" v-slot="{ componentField }" name="stopPrice">
        <FormItem>
          <FormLabel
            for="stopPrice"
            class="text-xs font-medium text-slate-300 flex items-center gap-1"
          >
            <Icon icon="lucide:dollar-sign" width="14" height="14" class="text-slate-400" />
            Est. Stop Loss
          </FormLabel>
          <Input
            type="number"
            v-bind="componentField"
            min="0"
            step="0.01"
            placeholder="0.00"
            class="bg-slate-800 border border-slate-600 text-slate-200 placeholder:text-slate-400 focus-visible:ring-emerald-500 focus-visible:border-emerald-500"
          />
          <FormMessage class="text-red-500" />
        </FormItem>
      </FormField>
      <QtyField />
    </div>

    <NoteField />
  </div>
</template>
