<script lang="ts" setup>
import { FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'

import { Icon } from '@iconify/vue'
import type { ScalePlanCreate } from '@/interfaces'

const { isEntry, plan } = defineProps<{
  isEntry: boolean
  plan: ScalePlanCreate
}>()

const emit = defineEmits<{
  remove: [plan: ScalePlanCreate]
}>()
</script>

<template>
  <PlanFormHeader :is-entry="isEntry" @remove="emit('remove', plan)" />
  <div class="space-y-4">
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <FormField class="space-y-2" v-slot="{ componentField }" name="orderType">
        <FormItem>
          <FormLabel for="orderType" class="text-xs font-medium text-slate-300"
            >Order Type</FormLabel
          >
          <Select v-bind="componentField">
            <SelectTrigger class="w-full bg-slate-800 border border-slate-600 text-slate-200">
              <SelectValue placeholder="Market" />
            </SelectTrigger>
            <SelectContent class="bg-slate-800 border-slate-600">
              <SelectGroup>
                <SelectItem value="market" class="text-slate-200 focus:bg-slate-700"
                  >Market</SelectItem
                >
                <SelectItem value="limit" class="text-slate-200 focus:bg-slate-700"
                  >Limit</SelectItem
                >
                <SelectItem value="stop" class="text-slate-200 focus:bg-slate-700">Stop</SelectItem>
                <SelectItem value="stop-limit" class="text-slate-200 focus:bg-slate-700"
                  >Stop Limit</SelectItem
                >
              </SelectGroup>
            </SelectContent>
          </Select>
          <FormMessage class="text-red-500" />
        </FormItem>
      </FormField>

      <FormField class="space-y-2" v-slot="{ componentField }" name="orderType">
        <FormItem>
          <FormLabel for="tradeType" class="text-xs font-medium text-slate-300"
            >Trade Type</FormLabel
          >
          <Select v-bind="componentField">
            <SelectTrigger class="w-full bg-slate-800 border border-slate-600 text-slate-200">
              <SelectValue placeholder="Long" />
            </SelectTrigger>
            <SelectContent class="bg-slate-800 border-slate-600">
              <SelectGroup>
                <SelectItem value="long" class="text-slate-200 focus:bg-slate-700">long</SelectItem>
                <SelectItem value="short" class="text-slate-200 focus:bg-slate-700"
                  >Short</SelectItem
                >
              </SelectGroup>
            </SelectContent>
          </Select>
          <FormMessage class="text-red-500" />
        </FormItem>
      </FormField>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <FormField class="space-y-2" v-slot="{ componentField }" name="qty">
        <FormItem>
          <FormLabel for="qty" class="text-xs font-medium text-slate-300 flex items-center gap-1">
            <Icon icon="lucide:hash" width="14" height="14" class="text-slate-400" />
            Quantity
          </FormLabel>
          <Input
            type="number"
            v-bind="componentField"
            min="1"
            placeholder="Shares"
            class="w-full bg-slate-800 border border-slate-600 text-slate-200 placeholder:text-slate-400 focus-visible:ring-emerald-500 focus-visible:border-emerald-500"
          />
          <FormMessage class="text-red-500" />
        </FormItem>
      </FormField>

      <FormField class="space-y-2" name="targetPrice" v-slot="{ componentField }">
        <FormItem>
          <FormLabel
            for="targetPrice"
            class="text-xs font-medium text-slate-300 flex items-center gap-1"
          >
            <Icon icon="lucide:dollar-sign" width="14" height="14" class="text-slate-400" />
            Est. Target Price
          </FormLabel>
          <Input
            type="number"
            v-bind="componentField"
            min="0"
            step="0.01"
            placeholder="0.00"
            class="w-full bg-slate-800 border border-slate-600 text-slate-200 placeholder:text-slate-400 focus-visible:ring-emerald-500 focus-visible:border-emerald-500"
          />
          <FormMessage class="text-red-500" />
        </FormItem>
      </FormField>
    </div>

    <FormField class="space-y-2" name="notes" v-slot="{ componentField }">
      <FormItem>
        <FormLabel for="notes" class="text-xs font-medium text-slate-300">Notes</FormLabel>
        <Textarea
          v-bind="componentField"
          placeholder="Notes for this entry plan..."
          rows="3"
          class="w-full bg-slate-800 border border-slate-600 text-slate-200 placeholder:text-slate-400 resize-none focus-visible:ring-emerald-500 focus-visible:border-emerald-500"
        />
        <FormMessage class="text-red-500" />
      </FormItem>
    </FormField>
  </div>
</template>
