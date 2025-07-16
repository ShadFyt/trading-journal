<script setup lang="ts">
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import { Button } from '@/components/ui/button'

import { FormField } from '../ui/form'
import { toTypedSchema } from '@vee-validate/zod'
import { tradeIdeaSchema } from '@/schemas'
import { useFieldArray, useForm } from 'vee-validate'

defineProps<{ close: () => void }>()

const formSchema = toTypedSchema(tradeIdeaSchema)
const { isFieldDirty, handleSubmit } = useForm({
  validationSchema: formSchema,
  initialValues: {
    targetPrices: [] as number[],
    symbol: '',
    entryMin: 0,
  },
})

const { fields, push, remove } = useFieldArray<number>('targetPrices');


const onSubmit = handleSubmit(async (values) => {
  try {
    console.log('submit', values)
  } catch (error) {
    console.error(error)
  }
})

const addPrice = () => {
  push(0);
};

const removePrice = (index: number) => {
  remove(index);
};
</script>

<template>
  <form :validation-schema="formSchema" class="w-full grid grid-cols-2 gap-6" @submit="onSubmit">
    <div class="col-span-2">
      <FormField v-slot="{ componentField }" name="symbol" :validate-on-blur="!isFieldDirty">
        <FormItem>
          <FormLabel for="symbol" class="block text-sm font-medium text-gray-700">Symbol</FormLabel>
          <FormControl>
            <Input type="text" id="symbol" placeholder="e.g. AAP L" v-bind="componentField" />
          </FormControl>
        </FormItem>
        <FormMessage />

      </FormField>
    </div>
    <FormField v-slot="{ componentField }" name="entryMin" :validate-on-blur="!isFieldDirty">
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
    <FormField v-slot="{ componentField }" name="entryMax" :validate-on-blur="!isFieldDirty">
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
    <div class="col-span-2">
    <FormField v-slot="{ componentField }" name="targetPrices" :validate-on-blur="!isFieldDirty">
      <FormItem>
        <FormLabel class="block text-sm font-medium text-gray-700">Target Prices</FormLabel>
        <FormControl>
          <div
            v-for="(price, index) in fields"
            :key="index"
            class="flex items-center mb-2"
          ><span class="mr-2">T{{ index + 1 }}</span>
            <Input
              type="number"
              placeholder="e.g. 150.50"
              class="mr-2"
              v-model="price.value"
            />
            <Button type="button" @click="removePrice(index)" variant="destructive">Remove</Button>
          </div>
          <Button type="button" @click="addPrice" variant="ghost">Add Price</Button>
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>
  </div>
    <div class="col-span-2">
      <FormField v-slot="{ componentField }" name="catalysts" :validate-on-blur="!isFieldDirty">
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
    <div class="col-span-2">
      <FormField v-slot="{ componentField }" name="notes" :validate-on-blur="!isFieldDirty">
        <FormItem>
          <FormLabel for="notes" class="block text-sm font-medium text-gray-700">Notes</FormLabel>
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
    <Button variant="outline" @click="close">Cancel</Button>
    <Button type="submit">Save</Button>
  </form>
</template>
