<script lang="ts" setup>
import { ScaleTradeTypeEnum } from '@/enums'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
</script>

<template>
  <!-- Label -->
  <div class="md:col-span-6">
    <FormField name="label" v-slot="{ componentField }">
      <FormItem>
        <FormLabel for="label">Label</FormLabel>
        <Input
          id="label"
          type="text"
          class="w-full"
          v-bind="componentField"
          placeholder="T1(Target 1)"
        />
        <FormMessage />
      </FormItem>
    </FormField>
  </div>

  <div class="md:col-span-6">
    <FormField name="targetPrice" v-slot="{ componentField }">
      <FormItem>
        <FormLabel for="targetPrice">Target Price</FormLabel>
        <Input
          id="targetPrice"
          type="number"
          step="0.01"
          inputmode="decimal"
          class="w-full"
          v-bind="componentField"
          placeholder="e.g. 160.00"
        />
        <FormMessage />
      </FormItem>
    </FormField>
  </div>

  <div class="md:col-span-6">
    <FormField name="tradeType" v-slot="{ componentField }">
      <FormItem>
        <FormLabel for="tradeType">Trade Type</FormLabel>
        <Select v-bind="componentField">
          <FormControl>
            <SelectTrigger id="tradeType" class="w-full">
              <SelectValue placeholder="Select type" />
            </SelectTrigger>
          </FormControl>
          <SelectContent>
            <SelectItem v-for="type in ScaleTradeTypeEnum.enum" :key="type" :value="type">
              {{ type }}
            </SelectItem>
          </SelectContent>
        </Select>
        <FormMessage />
      </FormItem>
    </FormField>
  </div>

  <!-- Value -->
  <div class="md:col-span-6">
    <FormField name="qty" v-slot="{ componentField }">
      <FormItem>
        <FormLabel for="qty">Quantity</FormLabel>
        <Input
          id="qty"
          type="number"
          step="1"
          min="1"
          class="w-full"
          v-bind="componentField"
          placeholder="e.g. 100"
        />
        <FormMessage />
      </FormItem>
    </FormField>
  </div>
  <!-- Notes -->
  <div class="md:col-span-12">
    <FormField name="notes" v-slot="{ componentField }">
      <FormItem>
        <FormLabel for="notes">Notes</FormLabel>
        <Textarea
          id="notes"
          rows="2"
          class="w-full"
          v-bind="componentField"
          placeholder="Optional notes for this plan"
        />
        <FormMessage />
      </FormItem>
    </FormField>
  </div>
</template>
