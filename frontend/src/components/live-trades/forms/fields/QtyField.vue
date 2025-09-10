<script lang="ts" setup>
import { Icon } from '@iconify/vue'
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import type { ScalePlanCreate } from '@/interfaces'

const qty = defineModel<ScalePlanCreate['qty']>()
</script>
<template>
  <FormField class="space-y-2" name="qty">
    <FormItem>
      <FormLabel for="qty" class="text-xs font-medium text-slate-300 flex items-center gap-1">
        <Icon icon="lucide:hash" width="14" height="14" class="text-slate-400" />
        Quantity
      </FormLabel>
      <Input
        type="number"
        v-model="qty"
        min="1"
        placeholder="Shares"
        class="w-full bg-slate-800 border border-slate-600 text-slate-200 placeholder:text-slate-400 focus-visible:ring-emerald-500 focus-visible:border-emerald-500"
      />
      <FormMessage class="text-red-500" />
    </FormItem>
  </FormField>
</template>
