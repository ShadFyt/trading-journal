<script setup lang="ts">
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'

defineProps<{
  isFieldDirty: boolean
}>()

</script>

<template>
  <div class="col-span-2">
    <FormField v-slot="{ componentField }" name="entryMin" :validate-on-blur="!isFieldDirty">
      <FormItem>
        <FormLabel for="entryMin" class="block text-sm font-medium text-gray-700">
          Entry Min
        </FormLabel>
        <Input
          type="number"
          id="entryMin"
          v-bind="componentField"
          placeholder="e.g. 150.50"
          step="0.01"
        />
      </FormItem>
    </FormField>
  </div>
  <div class="col-span-2">
    <FormField v-slot="{ componentField }" name="entryMax">
      <FormItem>
        <FormLabel for="entryMax" class="block text-sm font-medium text-gray-700">
          Entry Max
        </FormLabel>
        <Input
          type="number"
          id="entryMax"
          v-bind="componentField"
          placeholder="e.g. 150.50"
          step="0.01"
        />
      </FormItem>
    </FormField>
  </div>
  <div class="col-span-2">
    <FormField v-slot="{ componentField }" name="stop" :validate-on-blur="!isFieldDirty">
      <FormItem>
        <FormLabel for="stop" class="block text-sm font-medium text-gray-700">Stop Loss</FormLabel>
        <Input
          type="number"
          id="stop"
          v-bind="componentField"
          placeholder="e.g. 150.50"
          step="0.01"
        />
      </FormItem>
    </FormField>
  </div>
  <div class="col-span-6">
    <TargetPriceField :isFieldDirty="isFieldDirty" />
  </div>
</template>
