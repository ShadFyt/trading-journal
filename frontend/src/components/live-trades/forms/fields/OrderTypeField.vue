<script lang="ts" setup>
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
const { planId } = defineProps<{ planId: string }>()
</script>
<template>
  <FormField :name="`${planId}.orderType`" class="space-y-2" v-slot="{ value, setValue }">
    <FormItem>
      <FormLabel :for="`${planId}.orderType`" class="text-xs font-medium text-slate-300"
        >Order Type</FormLabel
      >
      <Select :model-value="value" @update:model-value="setValue">
        <SelectTrigger class="w-full bg-slate-800 border border-slate-600 text-slate-200">
          <SelectValue placeholder="Market" />
        </SelectTrigger>
        <SelectContent class="bg-slate-800 border-slate-600">
          <SelectGroup>
            <SelectItem value="market" class="text-slate-200 focus:bg-slate-700">Market</SelectItem>
            <SelectItem value="limit" class="text-slate-200 focus:bg-slate-700">Limit</SelectItem>
            <SelectItem value="stop" class="text-slate-200 focus:bg-slate-700">Stop</SelectItem>
            <SelectItem value="stop-limit" class="text-slate-200 focus:bg-slate-700"
              >Stop Limit</SelectItem
            >
          </SelectGroup>
        </SelectContent>
      </Select>
      <FormMessage class="text-red-500" />
    </FormItem>
  </FormField>
</template>
