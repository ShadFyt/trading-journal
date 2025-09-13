<script lang="ts" setup>
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
</script>

<template>
  <FormField name="label" v-slot="{ componentField }">
    <FormItem class="md:col-span-6">
      <FormLabel for="label">Label</FormLabel>
      <Input
        id="label"
        type="text"
        class="bg-slate-800 border border-slate-600 text-slate-200 placeholder:text-slate-400"
        v-bind="componentField"
        placeholder="T1(Target 1)"
      />
      <FormMessage />
    </FormItem>
  </FormField>

  <FormField name="targetPrice" v-slot="{ componentField }">
    <FormItem class="md:col-span-6">
      <FormLabel for="targetPrice">Target Price</FormLabel>
      <Input
        id="targetPrice"
        type="number"
        step="0.01"
        inputmode="decimal"
        class="bg-slate-800 border border-slate-600 text-slate-200 placeholder:text-slate-400"
        v-bind="componentField"
        placeholder="e.g. 160.00"
      />
      <FormMessage />
    </FormItem>
  </FormField>

  <div class="md:col-span-6">
    <OrderTypeField />
  </div>
  <div class="md:col-span-6">
    <QtyField />
  </div>
  <div class="md:col-span-12">
    <NoteField />
  </div>
</template>
