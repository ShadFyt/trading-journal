<script setup lang="ts">
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import type { TradeIdeaFormValues } from '@/interfaces/trade-idea.type'
import type { FormActions } from 'vee-validate'

interface Props {
  setFieldValue: FormActions<TradeIdeaFormValues>['setFieldValue']
  isFieldDirty: boolean
}

const { setFieldValue, isFieldDirty } = defineProps<Props>()
</script>

<template>
  <div class="col-span-6">
    <FormField v-slot="{ componentField }" name="symbol" :validate-on-blur="!isFieldDirty">
      <FormItem>
        <FormLabel for="symbol" class="block text-sm font-medium text-gray-700">Symbol</FormLabel>
        <FormControl>
          <Input type="text" id="symbol" placeholder="e.g. AAP L" v-bind="componentField" />
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>
  </div>
  <div class="col-span-4">
    <FormField v-slot="{ componentField }" name="setup" :validate-on-blur="!isFieldDirty">
      <FormItem>
        <FormLabel for="setup" class="block text-sm font-medium text-gray-700">Setup</FormLabel>
        <FormControl>
          <Input type="text" id="setup" placeholder="e.g. Breakout" v-bind="componentField" />
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>
  </div>
  <div class="col-span-2">
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
          >
            <NumberFieldContent>
              <NumberFieldDecrement />
              <NumberFieldInput />
              <NumberFieldIncrement />
            </NumberFieldContent>
          </NumberField>
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>
  </div>
</template>
