<script lang="ts" setup>
import { FormField, FormItem, FormLabel } from '../../ui/form'
import { useLiveTradeFormEdit } from '@/composables/forms/useLiveTradeFormEdit.ts'
import type { LiveTrade, LiveTradeUpdate } from '@/interfaces/trade.type.ts'
import { typedDateField } from '@/utils/typed-component.util.ts'
const { trade, isOpen, close, formType } = defineProps<{
  trade: LiveTrade
  isOpen: boolean
  close: (v: boolean) => void
  formType: 'edit' | 'close'
}>()

const { isFieldDirty, onSubmit, setFieldValue, isSubmitting, schema, onDelete } =
  useLiveTradeFormEdit(trade, formType, close)

const LiveTradeDateField = typedDateField<LiveTradeUpdate>()

const isCloseForm = computed(() => {
  if (formType === 'close') return true
  return trade.status === 'closed'
})
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
          <div :class="isCloseForm ? 'col-span-3' : 'col-span-6'">
            <LiveTradeDateField
              name="enterDate"
              title="Entry Date"
              :setFieldValue="setFieldValue"
            />
          </div>
          <CloseOutField
            v-if="isCloseForm"
            :setFieldValue="setFieldValue"
            :isFieldDirty="isFieldDirty"
          />
        </section>
        <SheetFooter class="flex flex-row justify-end">
          <Button
            :class="formType === 'close' ? 'w-1/2' : 'w-full'"
            :disabled="isSubmitting"
            type="submit"
            >{{ formType === 'close' ? 'Close Trade' : 'Save' }}</Button
          >
          <Button
            class="w-1/2"
            variant="destructive"
            v-if="formType === 'close'"
            :disabled="isSubmitting"
            type="button"
            @click="onDelete"
            >Delete Trade</Button
          >
        </SheetFooter>
      </form>
    </SheetContent>
  </Sheet>
</template>
