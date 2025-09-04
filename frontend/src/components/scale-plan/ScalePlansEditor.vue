<script setup lang="ts">
import { useFieldArray } from 'vee-validate'
import { computed } from 'vue'
import { FormField, FormItem, FormLabel, FormMessage, FormControl } from '@/components/ui/form'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { ScalePlanTypeEnum } from '@/enums/scale-plan.enum'
import type { ScalePlanCreate } from '@/interfaces'

const { fields, push, remove } = useFieldArray<ScalePlanCreate>('scalePlans')

function addPlan() {
  push({
    label: '',
    planType: ScalePlanTypeEnum.enum.TARGET,
    orderType: 'limit',
    qty: 1,
    targetPrice: undefined,
    stopPrice: undefined,
    limitPrice: undefined,
    goodTillDate: undefined,
    notes: '',
  })
}

const hasPlans = computed(() => fields.value.length > 0)
</script>

<template>
  <section class="col-span-6">
    <div class="flex items-center justify-between mb-2">
      <h3 id="scale-plans-heading" class="text-base font-semibold">Scale Plans</h3>
      <Button
        size="sm"
        type="button"
        class="focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
        @click="addPlan"
      >
        Add plan
      </Button>
    </div>

    <p v-if="!hasPlans" class="text-sm text-gray-600 mb-3">
      No scale plans yet. Click “Add plan” to create one.
    </p>

    <div
      class="space-y-3 max-h-[45vh] overflow-y-auto pr-1"
      role="region"
      aria-labelledby="scale-plans-heading"
    >
      <div
        v-for="(row, idx) in fields"
        :key="row.key"
        class="rounded-lg border bg-white p-3 md:p-4 shadow-sm"
      >
        <!-- Card header with actions -->
        <div class="flex items-center justify-between mb-2">
          <h4 class="text-sm font-medium">Plan {{ idx + 1 }}</h4>
          <Button
            type="button"
            variant="destructive"
            size="sm"
            class="h-9 min-w-[44px] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2"
            :aria-label="`Remove plan ${idx + 1}`"
            @click="remove(idx)"
          >
            Remove
          </Button>
        </div>

        <div class="grid grid-cols-1 gap-3 md:grid-cols-12">
          <!-- Label -->
          <div class="md:col-span-6">
            <FormField :name="`scalePlans[${idx}].label`" v-slot="{ componentField }">
              <FormItem>
                <FormLabel :for="`sp-label-${idx}`">Label</FormLabel>
                <Input
                  :id="`sp-label-${idx}`"
                  type="text"
                  class="w-full"
                  v-bind="componentField"
                  placeholder="e.g. First trim"
                />
                <FormMessage />
              </FormItem>
            </FormField>
          </div>

          <!-- Optional target price (for display/UX if you keep it in schema) -->
          <div class="md:col-span-6">
            <FormField :name="`scalePlans[${idx}].targetPrice`" v-slot="{ componentField }">
              <FormItem>
                <FormLabel :for="`sp-target-${idx}`">Target Price</FormLabel>
                <Input
                  :id="`sp-target-${idx}`"
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

          <!-- Kind -->
          <div class="md:col-span-6">
            <FormField :name="`scalePlans[${idx}].kind`" v-slot="{ componentField }">
              <FormItem>
                <FormLabel :for="`sp-plan-type-${idx}`">Plan Type</FormLabel>
                <Select v-bind="componentField">
                  <FormControl>
                    <SelectTrigger :id="`sp-plan-type-${idx}`" class="w-full">
                      <SelectValue placeholder="Select plan type" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem v-for="type in ScalePlanTypeEnum.enum" :key="type" :value="type">
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
            <FormField :name="`scalePlans[${idx}].value`" v-slot="{ componentField }">
              <FormItem>
                <FormLabel :for="`sp-value-${idx}`">Value</FormLabel>
                <Input
                  :id="`sp-value-${idx}`"
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
            <FormField :name="`scalePlans[${idx}].notes`" v-slot="{ componentField }">
              <FormItem>
                <FormLabel :for="`sp-notes-${idx}`">Notes</FormLabel>
                <Textarea
                  :id="`sp-notes-${idx}`"
                  rows="2"
                  class="w-full"
                  v-bind="componentField"
                  placeholder="Optional notes for this plan"
                />
                <FormMessage />
              </FormItem>
            </FormField>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
