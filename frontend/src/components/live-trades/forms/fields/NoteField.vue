<script lang="ts" setup>
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
const { planId } = defineProps<{ planId: string }>()
</script>

<template>
  <FormField class="space-y-2" :name="`${planId}.notes`" v-slot="{ value, setValue }">
    <FormItem>
      <FormLabel :for="`${planId}.notes`" class="text-xs font-medium text-slate-300"
        >Notes
      </FormLabel>
      <Textarea
        :model-value="value"
        @update:model-value="setValue"
        placeholder="Notes for this entry plan..."
        rows="3"
        class="w-full bg-slate-800 border border-slate-600 text-slate-200 placeholder:text-slate-400 resize-none"
      />
      <FormMessage class="text-red-500" />
    </FormItem>
  </FormField>
</template>
