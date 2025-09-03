<script lang="ts" setup>
import type { ScalePlan } from '@/interfaces'
import { toTypedSchema } from '@vee-validate/zod'
import { ExecutionCreateSchema } from '@/schemas/execution.schema.ts'
import { useForm } from 'vee-validate'
import { EXECUTION_SIDE, EXECUTION_SOURCE, ExecutionSideEnum, ExecutionSourceEnum } from '@/enums'
import { FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { useTradeExecutionMutations } from '@/composables'

const { scalePlan } = defineProps<{ scalePlan: ScalePlan }>()
const $emit = defineEmits<{
  (e: 'close'): void
}>()

const { executePlanMutation } = useTradeExecutionMutations()

const formSchema = toTypedSchema(ExecutionCreateSchema)
const { isSubmitting, handleSubmit } = useForm({
  validationSchema: formSchema,
  initialValues: {
    liveTradeId: scalePlan.liveTradeId,
    scalePlanId: scalePlan.id,
    side: ExecutionSideEnum.enum.SELL,
    source: ExecutionSourceEnum.enum.MANUAL,
    notes: '',
    commission: 1,
    price: scalePlan.targetPrice,
    qty: scalePlan.qty,
  },
})

const onSubmit = handleSubmit(async (values) => {
  executePlanMutation.mutate(values, {
    onSuccess() {
      $emit('close')
    },
  })
})
</script>

<template>
  <p class="text-xs font-semibold text-center mb-3">Execute scale plan {{ scalePlan.label }}</p>
  <form :validation-schema="formSchema" class="flex flex-col h-full relative" @submit="onSubmit">
    <FormLoadingSpinner :isSubmitting="isSubmitting" />
    <div class="grid grid-cols-1 gap-3 md:grid-cols-12">
      <div class="md:col-span-6">
        <FormField name="price" v-slot="{ componentField }">
          <FormItem>
            <FormLabel for="price">Price</FormLabel>
            <Input
              id="price"
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
        <FormField name="qty" v-slot="{ componentField }">
          <FormItem>
            <FormLabel for="qty">Shares</FormLabel>
            <Input
              id="qty"
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
        <FormField name="side" v-slot="{ componentField }">
          <FormItem>
            <FormLabel for="side">Action</FormLabel>
            <Select v-bind="componentField">
              <FormControl>
                <SelectTrigger id="side" class="w-full">
                  <SelectValue placeholder="Select side" />
                </SelectTrigger>
              </FormControl>
              <SelectContent>
                <SelectItem v-for="side in EXECUTION_SIDE" :key="side" :value="side">
                  {{ side }}
                </SelectItem>
              </SelectContent>
            </Select>
            <FormMessage />
          </FormItem>
        </FormField>
      </div>
      <div class="md:col-span-2">
        <FormField name="source" v-slot="{ componentField }">
          <FormItem>
            <FormLabel for="source">Method</FormLabel>
            <Select v-bind="componentField">
              <FormControl>
                <SelectTrigger id="source" class="w-full">
                  <SelectValue placeholder="Select Source" />
                </SelectTrigger>
              </FormControl>
              <SelectContent>
                <SelectItem v-for="side in EXECUTION_SOURCE" :key="side" :value="side">
                  {{ side }}
                </SelectItem>
              </SelectContent>
            </Select>
            <FormMessage />
          </FormItem>
        </FormField>
      </div>

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
    <Button type="submit" class="mt-3" :disabled="isSubmitting">
      Execute {{ scalePlan.label }} Scale Plan
    </Button>
  </form>
</template>
