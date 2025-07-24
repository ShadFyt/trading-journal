<script setup lang="ts">
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'

import { FormField, FormItem, FormLabel } from '../ui/form'
import { useTradeIdeaForm } from '@/composables'
import type { TradeIdea } from '@/interfaces/trade-idea.type'

const { selectedTrade, isOpen, close } = defineProps<{
  isOpen: boolean
  close: (v: boolean) => void
  selectedTrade?: TradeIdea | null
}>()

const {
  isEditMode,
  isFieldDirty,
  onSubmit,
  setFieldValue,
  isSubmitting,
  schema,
  isFormValid,
  hasFormChanged,
} = useTradeIdeaForm(close, selectedTrade)

const message = computed(() => {
  return isEditMode.value && selectedTrade
    ? `Update Trade Idea For ${selectedTrade.symbol}`
    : 'Add Trade Idea'
})
</script>

<template>
  <Sheet :open="isOpen" @update:open="close">
    <SheetTrigger v-if="!isEditMode" as-child>
      <slot name="trigger-button" />
    </SheetTrigger>
    <SheetContent :class="{ 'opacity-50': isSubmitting, 'pointer-events-none': isSubmitting }">
      <form class="flex flex-col h-full relative" :validation-schema="schema" @submit="onSubmit">
        <!-- Loading spinner -->

        <div v-if="isSubmitting" class="absolute inset-0 flex items-center justify-center z-50">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>

        <section class="w-full grid grid-cols-6 p-2 space-x-2 gap-1">
          <SheetHeader class="col-span-6">
            <SheetTitle class="text-lg">{{ message }}</SheetTitle>
            <SheetDescription> Click save when you're done. </SheetDescription>
          </SheetHeader>
          <BasicFields :setFieldValue="setFieldValue" :isFieldDirty="isFieldDirty" />
          <EditModeFields
            v-if="isEditMode && selectedTrade"
            :setFieldValue="setFieldValue"
            :isFieldDirty="isFieldDirty"
          />
          <PriceFields :isFieldDirty="isFieldDirty" />
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
          <Button :disabled="isSubmitting || !isFormValid || !hasFormChanged" type="submit">{{
            isEditMode ? 'Update' : 'Save'
          }}</Button>
        </SheetFooter>
      </form>
    </SheetContent>
  </Sheet>
</template>
