<script setup lang="ts">
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'

import { FormField, FormItem, FormLabel, FormMessage } from '../ui/form'
import { toTypedSchema } from '@vee-validate/zod'
import { tradeIdeaCreateSchema } from '@/schemas'
import { useFieldArray, useForm } from 'vee-validate'
import { useTradeIdeaMutationService } from '@/composables'
import type { TradeIdea } from '@/interfaces/trade-idea.type'

const { createMutation } = useTradeIdeaMutationService()
const formSchema = toTypedSchema(tradeIdeaCreateSchema)

const {
  selectedTrade,
  isOpen = null,
  close,
} = defineProps<{
  selectedTrade?: TradeIdea | null
  isOpen?: boolean | null
  close?: (v: boolean) => void
}>()

const { isFieldDirty, handleSubmit, setFieldValue, isSubmitting } = useForm({
  validationSchema: formSchema,
  initialValues: {
    targetPrices: [] as number[],
    symbol: selectedTrade?.symbol ?? '',
    entryMin: 0,
    ...(selectedTrade ? selectedTrade : {}),
  },
})
const { fields, push, remove } = useFieldArray<number>('targetPrices')

const message = computed(() => {
  if (selectedTrade) {
    return `Update Trade Idea For ${selectedTrade.symbol}`
  }
  return 'Add Trade Idea'
})

const sheetListeners = computed(() => {
  return isOpen !== null && close ? { 'update:open': close } : {}
})

const onSubmit = handleSubmit(async (values) => {
  console.log('submit', values)
  try {
    await createMutation.mutateAsync(values)
  } catch (error) {
    console.error(error)
  }
})

const addPrice = () => {
  push(0)
}

const removePrice = (index: number) => {
  remove(index)
}

const getSheetProps = () => {
  return isOpen ? { open: isOpen } : {}
}
</script>

<template>
  <Sheet v-bind="getSheetProps()" v-on="sheetListeners">
    <SheetTrigger v-if="!isOpen" as-child>
      <slot name="trigger-button" />
    </SheetTrigger>
    <SheetContent :class="{ 'opacity-50': isSubmitting, 'pointer-events-none': isSubmitting }">
      <form
        class="flex flex-col h-full relative"
        :validation-schema="formSchema"
        @submit="onSubmit"
      >
        <!-- Loading spinner -->

        <div v-if="isSubmitting" class="absolute inset-0 flex items-center justify-center z-50">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>

        <section class="w-full grid grid-cols-6 p-2 space-x-2 gap-1">
          <SheetHeader class="col-span-6">
            <SheetTitle class="text-lg">{{ message }}</SheetTitle>
            <SheetDescription> Click save when you're done. </SheetDescription>
          </SheetHeader>
          <div class="col-span-6">
            <FormField v-slot="{ componentField }" name="symbol" :validate-on-blur="!isFieldDirty">
              <FormItem>
                <FormLabel for="symbol" class="block text-sm font-medium text-gray-700"
                  >Symbol</FormLabel
                >
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
                <FormLabel for="setup" class="block text-sm font-medium text-gray-700"
                  >Setup</FormLabel
                >
                <FormControl>
                  <Input
                    type="text"
                    id="setup"
                    placeholder="e.g. Breakout"
                    v-bind="componentField"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            </FormField>
          </div>
          <div class="col-span-2">
            <FormField v-slot="{ value }" name="rating" :validate-on-blur="!isFieldDirty">
              <FormItem>
                <FormLabel for="rating" class="block text-sm font-medium text-gray-700"
                  >Rating</FormLabel
                >
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
          <div class="col-span-2">
            <FormField
              v-slot="{ componentField }"
              name="entryMin"
              :validate-on-blur="!isFieldDirty"
            >
              <FormItem>
                <FormLabel for="entry-min" class="block text-sm font-medium text-gray-700">
                  Entry Min
                </FormLabel>
                <Input
                  type="number"
                  id="entry-min"
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
              name="entryMax"
              :validate-on-blur="!isFieldDirty"
            >
              <FormItem>
                <FormLabel for="entry-max" class="block text-sm font-medium text-gray-700">
                  Entry Max
                </FormLabel>
                <Input
                  type="number"
                  id="entry-max"
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
                <FormLabel for="stop" class="block text-sm font-medium text-gray-700"
                  >Stop Loss</FormLabel
                >
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
            <FormField name="targetPrices" :validate-on-blur="!isFieldDirty">
              <FormItem>
                <FormLabel class="block text-sm font-medium text-gray-700">Target Prices</FormLabel>
                <FormControl>
                  <div v-for="(price, index) in fields" :key="index" class="flex items-center mb-2">
                    <span class="mr-2">T{{ index + 1 }}</span>
                    <Input
                      type="number"
                      placeholder="e.g. 150.50"
                      class="mr-2"
                      v-model="price.value"
                      step="0.01"
                    />
                    <Button type="button" @click="removePrice(index)" variant="destructive"
                      >Remove</Button
                    >
                  </div>
                  <Button type="button" @click="addPrice" variant="ghost">Add Price</Button>
                </FormControl>
                <FormMessage />
              </FormItem>
            </FormField>
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
