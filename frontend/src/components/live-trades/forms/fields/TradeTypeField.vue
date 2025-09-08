<script lang="ts" setup>
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
</script>

<template>
  <FormField class="space-y-2" v-slot="{ componentField }" name="tradeType">
    <FormItem>
      <FormLabel for="tradeType" class="text-xs font-medium text-slate-300">Trade Type</FormLabel>
      <Select v-bind="componentField">
        <SelectTrigger class="w-full bg-slate-800 border border-slate-600 text-slate-200">
          <SelectValue placeholder="Long" />
        </SelectTrigger>
        <SelectContent class="bg-slate-800 border-slate-600">
          <SelectGroup>
            <SelectItem value="long" class="text-slate-200 focus:bg-slate-700">long</SelectItem>
            <SelectItem value="short" class="text-slate-200 focus:bg-slate-700">Short</SelectItem>
          </SelectGroup>
        </SelectContent>
      </Select>
      <FormMessage class="text-red-500" />
    </FormItem>
  </FormField>
</template>
