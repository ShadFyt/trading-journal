<script lang="ts" setup>
import { Icon } from '@iconify/vue'
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'

const { planId } = defineProps<{ planId?: string }>()

const fieldName = computed(() => (planId ? `${planId}.qty` : 'qty'))
</script>
<template>
  <FormField class="space-y-2" :name="fieldName" v-slot="{ value, setValue }">
    <FormItem>
      <FormLabel
        :for="fieldName"
        class="text-xs font-medium text-slate-300 flex items-center gap-1"
      >
        <Icon icon="lucide:hash" width="14" height="14" class="text-slate-400" />
        Quantity
      </FormLabel>
      <Input
        type="number"
        :model-value="value"
        @update:model-value="setValue"
        min="1"
        placeholder="Shares"
        class="w-full bg-slate-800 border border-slate-600 placeholder:text-slate-400"
      />
      <FormMessage class="text-red-500" />
    </FormItem>
  </FormField>
</template>
