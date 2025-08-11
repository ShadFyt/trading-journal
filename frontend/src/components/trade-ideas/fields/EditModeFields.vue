<script setup lang="ts">
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import type { FormActions } from 'vee-validate'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { statusOptions } from '@/shared/status'
import type { TradeIdeaUpdate } from '@/interfaces/trade-idea.type'
import { typedDateField } from '@/utils/typed-component.util'

interface Props {
  setFieldValue: FormActions<TradeIdeaUpdate>['setFieldValue']
  isFieldDirty: (path: any) => boolean
  isLiveTrade: boolean
}

const { setFieldValue, isFieldDirty, isLiveTrade } = defineProps<Props>()

const TradeIdeaDateField = typedDateField<TradeIdeaUpdate>()
</script>

<template>
  <div class="col-span-4">
    <FormField v-slot="{ componentField }" name="status" :validate-on-blur="!isFieldDirty">
      <FormItem>
        <FormLabel for="status" class="block text-sm font-medium text-gray-700">Status</FormLabel>
        <Select v-bind="componentField" :disabled="isLiveTrade">
          <FormControl>
            <SelectTrigger class="w-full">
              <SelectValue placeholder="Select a status" />
            </SelectTrigger>
          </FormControl>
          <SelectContent>
            <SelectItem v-for="option in statusOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </SelectItem>
          </SelectContent>
        </Select>
        <FormMessage />
      </FormItem>
    </FormField>
  </div>
  <div class="col-span-2">
    <TradeIdeaDateField name="ideaDate" title="Idea Date" :setFieldValue="setFieldValue" />
  </div>
</template>
