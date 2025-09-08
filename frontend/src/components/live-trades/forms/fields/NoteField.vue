<script lang="ts" setup>
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
</script>

<template>
  <FormField class="space-y-2" name="notes" v-slot="{ componentField }">
    <FormItem>
      <FormLabel for="notes" class="text-xs font-medium text-slate-300">Notes</FormLabel>
      <Textarea
        v-bind="componentField"
        placeholder="Notes for this entry plan..."
        rows="3"
        class="w-full bg-slate-800 border border-slate-600 text-slate-200 placeholder:text-slate-400 resize-none focus-visible:ring-emerald-500 focus-visible:border-emerald-500"
      />
      <FormMessage class="text-red-500" />
    </FormItem>
  </FormField>
</template>
