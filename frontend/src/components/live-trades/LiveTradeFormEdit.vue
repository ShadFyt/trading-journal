<script lang="ts" setup>
import { FormField, FormItem, FormLabel } from '../ui/form'
import { useLiveTradeFormEdit } from '@/composables/useLiveTradeFormEdit'
import type { LiveTrade, LiveTradeUpdate } from '@/interfaces/live-trade.type'
import { typedDateField } from '@/utils/typed-component.util'
const { trade, isOpen, close } = defineProps<{
  trade: LiveTrade
  isOpen: boolean
  close: (v: boolean) => void
}>()

const { isFieldDirty, onSubmit, setFieldValue, isSubmitting, schema } = useLiveTradeFormEdit(trade)

const LiveTradeDateField = typedDateField<LiveTradeUpdate>()

const statusOptions = [
  { value: 'breakeven', label: 'Break Even' },
  { value: 'big win', label: 'Big Winner' },
  { value: 'small win', label: 'Small Winner' },
  { value: 'small loss', label: 'Small Loser' },
  { value: 'big loss', label: 'Big Loser' },
  { value: 'pending', label: 'Pending' },
]
</script>

<template>
  <Sheet :open="isOpen" @update:open="close">
    <SheetContent :class="{ 'opacity-50': isSubmitting, 'pointer-events-none': isSubmitting }">
      <form class="flex flex-col h-full relative" :validation-schema="schema" @submit="onSubmit">
        <!-- Loading spinner -->

        <div v-if="isSubmitting" class="absolute inset-0 flex items-center justify-center z-50">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>

        <section class="w-full grid grid-cols-6 p-2 space-x-2 gap-1">
          <SheetHeader class="col-span-6">
            <SheetTitle class="text-lg">Edit Live Trade</SheetTitle>
            <SheetDescription> Click save when you're done. </SheetDescription>
          </SheetHeader>
          <BasicFields :setFieldValue="setFieldValue" :isFieldDirty="isFieldDirty" />
          <div class="col-span-2">
            <FormField
              v-slot="{ componentField }"
              name="entryPriceAvg"
              :validate-on-blur="!isFieldDirty"
            >
              <FormItem>
                <FormLabel for="entryPriceAvg" class="block text-sm font-medium text-gray-700">
                  Entry Price Avg
                </FormLabel>
                <Input
                  type="number"
                  id="entryPriceAvg"
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
                <FormLabel for="stop" class="block text-sm font-medium text-gray-700">
                  Stop
                </FormLabel>
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
          <div class="col-span-2">
            <FormField
              v-slot="{ componentField }"
              name="positionSize"
              :validate-on-blur="!isFieldDirty"
            >
              <FormItem>
                <FormLabel for="positionSize" class="block text-sm font-medium text-gray-700">
                  Position Size
                </FormLabel>
                <Input
                  type="number"
                  id="positionSize"
                  v-bind="componentField"
                  placeholder="e.g. 100"
                  step="1"
                />
              </FormItem>
            </FormField>
          </div>
          <div class="col-span-3">
            <LiveTradeDateField
              name="enterDate"
              title="Entry Date"
              :setFieldValue="setFieldValue"
            />
          </div>
          <div class="col-span-3">
            <LiveTradeDateField name="exitDate" title="Exit Date" :setFieldValue="setFieldValue" />
          </div>
          <div class="col-span-6">
            <TargetPriceField :isFieldDirty="isFieldDirty" />
          </div>
          <div class="col-span-2">
            <FormField v-slot="{ componentField }" name="outcome" :validate-on-blur="!isFieldDirty">
              <FormItem>
                <FormLabel for="outcome" class="block text-sm font-medium text-gray-700"
                  >Outcome</FormLabel
                >
                <Select v-bind="componentField">
                  <FormControl>
                    <SelectTrigger class="w-full">
                      <SelectValue default-value="pending" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem
                      v-for="option in statusOptions"
                      :key="option.value"
                      :value="option.value"
                    >
                      {{ option.label }}
                    </SelectItem>
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            </FormField>
          </div>
          <div class="col-span-2">
            <FormField
              v-slot="{ componentField }"
              name="commissions"
              :validate-on-blur="!isFieldDirty"
            >
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
            <FormField
              v-slot="{ componentField }"
              name="exitPriceAvg"
              :validate-on-blur="!isFieldDirty"
            >
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
        </section>
        <SheetFooter class="flex justify-end">
          <Button :disabled="isSubmitting" type="submit">Save</Button>
        </SheetFooter>
      </form>
    </SheetContent>
  </Sheet>
</template>
