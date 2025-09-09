<script lang="ts" setup>
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { typedDateField } from '@/utils'
import type { LiveTradeCreate } from '@/interfaces'
import type { FormActions, GenericObject } from 'vee-validate'

const { setFieldValue, isFieldDirty } = defineProps<{
  setFieldValue: FormActions<GenericObject>['setFieldValue']
  isFieldDirty: (path: keyof LiveTradeCreate) => boolean
}>()
const TradeDateField = typedDateField<LiveTradeCreate>()
</script>

<template>
  <FormField v-slot="{ componentField }" name="symbol" class="space-y-2">
    <FormItem>
      <FormLabel for="symbol">Symbol *</FormLabel>
      <Input
        v-bind="componentField"
        placeholder="e.g. AAPL"
        class="uppercase border-slate-600 bg-slate-800"
      />
      <FormMessage class="text-red-500" />
    </FormItem>
  </FormField>

  <FormField name="setup" v-slot="{ componentField }" class="space-y-2">
    <FormItem>
      <FormLabel for="setup" class="text-slate-200">Setup Strategy</FormLabel>
      <Textarea
        v-bind="componentField"
        placeholder="Describe your trading setup and analysis..."
        rows="3"
        class="border-slate-600 bg-slate-800 resize-none"
      />
      <FormMessage class="text-red-500" />
    </FormItem>
  </FormField>

  <div class="grid grid-cols-2 gap-4">
    <FormField v-slot="{ value }" name="rating" :validate-on-blur="!isFieldDirty">
      <FormItem>
        <FormLabel for="rating" class="block text-sm font-medium text-gray-700">Rating</FormLabel>
        <FormControl>
          <NumberField
            id="rating"
            :min="1"
            :max="10"
            :step="0.1"
            :format-options="{
              style: 'decimal',
              minimumFractionDigits: 1,
            }"
            :model-value="value"
            @update:model-value="
              (v) => {
                if (v) {
                  setFieldValue('rating', v)
                } else {
                  setFieldValue('rating', undefined)
                }
              }
            "
            class="bg-slate-800"
          >
            <NumberFieldContent>
              <NumberFieldDecrement />
              <NumberFieldInput />
              <NumberFieldIncrement />
            </NumberFieldContent>
          </NumberField>
        </FormControl>
        <FormMessage class="text-red-500" />
      </FormItem>
    </FormField>

    <TradeDateField name="ideaDate" title="Entry Date" :setFieldValue="setFieldValue" />
  </div>
</template>
