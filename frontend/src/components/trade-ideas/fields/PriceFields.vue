<script setup lang="ts">
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { useFieldArray } from 'vee-validate'

defineProps<{
  isFieldDirty: boolean
}>()

const { fields, push, remove } = useFieldArray<number>('targetPrices')

const addPrice = () => {
  push(0)
}

const removePrice = (index: number) => {
  remove(index)
}
</script>

<template>
  <div class="col-span-2">
    <FormField v-slot="{ componentField }" name="entryMin" :validate-on-blur="!isFieldDirty">
      <FormItem>
        <FormLabel for="entryMin" class="block text-sm font-medium text-gray-700">
          Entry Min
        </FormLabel>
        <Input
          type="number"
          id="entryMin"
          v-bind="componentField"
          placeholder="e.g. 150.50"
          step="0.01"
        />
      </FormItem>
    </FormField>
  </div>
  <div class="col-span-2">
    <FormField v-slot="{ componentField }" name="entryMax">
      <FormItem>
        <FormLabel for="entryMax" class="block text-sm font-medium text-gray-700">
          Entry Max
        </FormLabel>
        <Input
          type="number"
          id="entryMax"
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
        <FormLabel for="stop" class="block text-sm font-medium text-gray-700">Stop Loss</FormLabel>
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
            <Button type="button" @click="removePrice(index)" variant="destructive">Remove</Button>
          </div>
          <Button type="button" @click="addPrice" variant="ghost">Add Price</Button>
        </FormControl>
        <FormMessage />
      </FormItem>
    </FormField>
  </div>
</template>
