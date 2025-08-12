<script lang="ts" setup>
import { FormField, FormItem, FormLabel } from '@/components/ui/form'
import type { FormActions, GenericObject } from 'vee-validate'
import { typedDateField } from '@/utils/typed-component.util'
import type { LiveTradeUpdate } from '@/interfaces'

defineProps<{
  setFieldValue: FormActions<GenericObject>['setFieldValue']
  isFieldDirty: (path: keyof LiveTradeUpdate) => boolean
}>()

const statusOptions = [
  { value: 'breakeven', label: 'Break Even' },
  { value: 'big win', label: 'Big Winner' },
  { value: 'small win', label: 'Small Winner' },
  { value: 'small loss', label: 'Small Loser' },
  { value: 'big loss', label: 'Big Loser' },
  { value: 'pending', label: 'Pending' },
]
const LiveTradeDateField = typedDateField<LiveTradeUpdate>()
</script>

<template>
  <div class="col-span-3">
    <LiveTradeDateField name="exitDate" title="Exit Date" :setFieldValue="setFieldValue" />
  </div>
  <div class="col-span-2">
    <FormField v-slot="{ componentField }" name="outcome" :validate-on-blur="!isFieldDirty">
      <FormItem>
        <FormLabel for="outcome" class="block text-sm font-medium text-gray-700">Outcome</FormLabel>
        <Select v-bind="componentField">
          <FormControl>
            <SelectTrigger class="w-full">
              <SelectValue default-value="pending" />
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
    <FormField v-slot="{ componentField }" name="commissions" :validate-on-blur="!isFieldDirty">
      <FormItem>
        <FormLabel for="commissions" class="block text-sm font-medium text-gray-700">
          Commission
        </FormLabel>
        <Input
          type="number"
          id="commissions"
          v-bind="componentField"
          placeholder="e.g. 100"
          step="1"
        />
      </FormItem>
    </FormField>
  </div>
  <div class="col-span-2">
    <FormField v-slot="{ componentField }" name="exitPriceAvg" :validate-on-blur="!isFieldDirty">
      <FormItem>
        <FormLabel for="exitPriceAvg" class="block text-sm font-medium text-gray-700">
          Exit Price Avg
        </FormLabel>
        <Input
          type="number"
          id="exitPriceAvg"
          v-bind="componentField"
          placeholder="e.g. 150.50"
          step="0.01"
        />
      </FormItem>
      <FormMessage />
    </FormField>
  </div>
</template>
