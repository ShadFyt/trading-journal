<script lang="ts" setup>
import { Icon } from '@iconify/vue'
import { useTradeFormCreate } from '@/composables'
import { typedDateField } from '@/utils'
import type { LiveTradeCreate } from '@/interfaces'
const { onSubmit, isFormValid, schema, setFieldValue, isFieldDirty } = useTradeFormCreate()
const TradeDateField = typedDateField<LiveTradeCreate>()
</script>

<template>
  <form :validation-schema="schema" class="h-screen w-96 flex flex-col">
    <header class="p-4 border-b border-slate-700 flex items-center justify-between">
      <h2 class="text-lg font-semibold">New Trade Idea</h2>
      <div class="flex gap-2">
        <Button variant="ghost" class="text-slate-400 hover:text-white" @click="$emit('cancel')">
          Cancel
        </Button>
        <Button :disabled="!isFormValid" class="gap-1" @click="onSubmit">
          <Icon icon="lucide:check" width="24" height="24" /> Save Trade
        </Button>
      </div>
    </header>

    <section class="flex-1 overflow-y-auto">
      <Card class="border-none bg-slate-900/60">
        <CardHeader>
          <CardTitle class="text-base text-slate-100">Basic Details</CardTitle>
        </CardHeader>
        <CardContent class="space-y-4">
          <FormField v-slot="{ componentField }" name="symbol" class="space-y-2">
            <FormItem>
              <FormLabel for="symbol" class="text-slate-200">Symbol *</FormLabel>
              <Input
                v-bind="componentField"
                placeholder="e.g. AAPL"
                class="uppercase border-slate-600 bg-slate-800"
              />
              <FormMessage />
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
              <FormMessage />
            </FormItem>
          </FormField>

          <div class="grid grid-cols-2 gap-4">
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
                    class="bg-slate-800"
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

            <TradeDateField name="ideaDate" title="Entry Date" :setFieldValue="setFieldValue" />
          </div>
          <BasicTradeField :set-field-value="setFieldValue" :is-field-dirty="isFieldDirty" />
        </CardContent>
      </Card>
    </section>
  </form>
</template>
