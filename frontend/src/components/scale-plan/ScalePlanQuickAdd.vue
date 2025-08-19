<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { Tooltip } from '@/components/ui/tooltip'
import { toTypedSchema } from '@vee-validate/zod'
import { ScalePlanCreateSchema } from '@/schemas'
import { useForm } from 'vee-validate'
import { SCALE_PLAN_KINDS } from '@/enums'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

const formSchema = toTypedSchema(ScalePlanCreateSchema)
const { isFieldDirty, isSubmitting } = useForm({
  validationSchema: formSchema,
})
</script>

<template>
  <Popover>
    <PopoverTrigger>
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger as-child>
            <Icon
              class="hover:opacity-80 cursor-pointer"
              icon="lucide:battery-plus"
              width="24"
              height="24"
            />
          </TooltipTrigger>
          <TooltipContent>
            <p class="text-xs font-semibold tracking-wide">Add Scale Plan</p>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    </PopoverTrigger>
    <PopoverContent>
      <p class="text-xs font-semibold text-center mb-3">Scale Out Plan</p>
      <form class="flex flex-col h-full relative" :validation-schema="formSchema">
        <!-- Loading spinner -->

        <div v-if="isSubmitting" class="absolute inset-0 flex items-center justify-center z-50">
          <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
        </div>

        <div class="grid grid-cols-1 gap-3 md:grid-cols-12">
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

          <!-- Optional target price (for display/UX if you keep it in schema) -->
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

          <!-- Kind -->
          <div class="md:col-span-6">
            <FormField name="kind" v-slot="{ componentField }">
              <FormItem>
                <FormLabel for="kind">Kind</FormLabel>
                <Select v-bind="componentField">
                  <FormControl>
                    <SelectTrigger id="kind" class="w-full">
                      <SelectValue placeholder="Select kind" />
                    </SelectTrigger>
                  </FormControl>
                  <SelectContent>
                    <SelectItem v-for="k in SCALE_PLAN_KINDS" :key="k" :value="k">
                      {{ k }}
                    </SelectItem>
                  </SelectContent>
                </Select>
                <FormMessage />
              </FormItem>
            </FormField>
          </div>

          <!-- Value -->
          <div class="md:col-span-6">
            <FormField name="value" v-slot="{ componentField }">
              <FormItem>
                <FormLabel for="value">Value</FormLabel>
                <Input
                  id="value"
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
        </div>
        <Button type="submit" class="mt-3" :disabled="!isFieldDirty('label') || isSubmitting">
          Add Scale Plan
        </Button>
      </form>
    </PopoverContent>
  </Popover>
</template>
