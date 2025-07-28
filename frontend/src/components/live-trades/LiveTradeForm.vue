<script setup lang="ts">
import { FormField, FormItem, FormLabel } from '../ui/form'
import { useLiveTradeForm } from '@/composables/useLiveTradeForm';
import type { TradeIdea } from '@/interfaces/trade-idea.type'

const { tradeIdea, isOpen, close } = defineProps<{ tradeIdea: TradeIdea, isOpen: boolean, close: (v: boolean) => void }>()

const {
  isFieldDirty,
  onSubmit,
  setFieldValue,
  isSubmitting,
  schema,
} = useLiveTradeForm(tradeIdea)
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
              <SheetTitle class="text-lg">Convert Trade Idea to Live Trade</SheetTitle>
              <SheetDescription> Click save when you're done. </SheetDescription>
            </SheetHeader>
            <BasicFields :setFieldValue="setFieldValue" :isFieldDirty="isFieldDirty" />
            <div class="col-span-2">
              <FormField v-slot="{ componentField }" name="entryPriceAvg" :validate-on-blur="!isFieldDirty">
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
              <FormField v-slot="{ componentField }" name="positionSize" :validate-on-blur="!isFieldDirty">
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
            <div class="col-span-6">
              <TargetPriceField :isFieldDirty="isFieldDirty" />
            </div>
            <div class="col-span-6">
              <FormField
                v-slot="{ componentField }"
                name="catalysts"
                :validate-on-blur="!isFieldDirty"
              >
                <FormItem>
                  <FormLabel for="catalysts" class="block text-sm font-medium text-gray-700"
                    >Catalysts</FormLabel
                  >
                  <FormControl>
                    <Textarea
                      id="catalysts"
                      rows="3"
                      v-bind="componentField"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                      placeholder="Add any catalysts news"
                    />
                  </FormControl>
                </FormItem>
              </FormField>
            </div>
            <div class="col-span-6">
              <FormField v-slot="{ componentField }" name="notes" :validate-on-blur="!isFieldDirty">
                <FormItem>
                  <FormLabel for="notes" class="block text-sm font-medium text-gray-700"
                    >Notes</FormLabel
                  >
                  <FormControl>
                    <Textarea
                      id="notes"
                      rows="3"
                      v-bind="componentField"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                      placeholder="Add any additional notes or analysis..."
                    />
                  </FormControl>
                </FormItem>
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
  