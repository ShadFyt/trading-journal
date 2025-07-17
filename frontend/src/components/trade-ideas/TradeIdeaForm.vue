<script setup lang="ts">
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'

import { FormField, FormItem, FormLabel, FormMessage } from '../ui/form'
import { toTypedSchema } from '@vee-validate/zod'
import { tradeIdeaCreateSchema } from '@/schemas'
import { useFieldArray, useForm } from 'vee-validate'

const formSchema = toTypedSchema(tradeIdeaCreateSchema)
const { isFieldDirty, handleSubmit } = useForm({
  validationSchema: formSchema,
  initialValues: {
    targetPrices: [] as number[],
    symbol: '',
    entryMin: 0,
  },
})

const { fields, push, remove } = useFieldArray<number>('targetPrices')

const onSubmit = handleSubmit(async (values) => {
  try {
    console.log('submit', values)
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
</script>

<template>
  <Sheet>
    <SheetTrigger as-child>
      <FabRoutingButton
        message="Add Trade Idea"
        iconName="lucide:plus"
        position="bottom-right"
        size="s"
      />
    </SheetTrigger>
    <SheetContent>
      <form class="flex flex-col h-full" :validation-schema="formSchema" @submit="onSubmit">
        <section class="w-full grid grid-cols-6 p-2 space-x-2">
          <SheetHeader class="col-span-6">
            <SheetTitle>Trade Ideas</SheetTitle>
            <SheetDescription>
              Add a new trade idea here. Click save when you're done.
            </SheetDescription>
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
            <FormField v-slot="{ componentField }" name="rrRatio" :validate-on-blur="!isFieldDirty">
              <FormItem>
                <FormLabel for="rr-ratio" class="block text-sm font-medium text-gray-700"
                  >R/R Ratio</FormLabel
                >
                <FormControl>
                  <Input
                    type="number"
                    id="rr-ratio"
                    placeholder="e.g. 2"
                    v-bind="componentField"
                    step="1"
                  />
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
          <Button class="col-span-6" type="submit"> Save changes </Button>
        </SheetFooter>
      </form>
    </SheetContent>
  </Sheet>
</template>
