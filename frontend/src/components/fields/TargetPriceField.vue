<script setup lang="ts">
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import { useFieldArray } from 'vee-validate'

defineProps<{ isFieldDirty: (path: any) => boolean }>()

const { fields, push, remove } = useFieldArray<number>('targetPrices')

const addPrice = () => {
  push(0)
}

const removePrice = (index: number) => {
  remove(index)
}
</script>

<template>
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
</template>
