<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { ScalePlanUpdateSchema } from '@/schemas'
import { useForm } from 'vee-validate'
import { useScalePlanMutationService } from '@/composables'
import { z } from 'zod'
import type { LiveTrade, ScalePlan } from '@/interfaces'

const { scalePlan, trade } = defineProps<{
  scalePlan: ScalePlan
  trade: LiveTrade
}>()

const $emit = defineEmits<{
  (e: 'close'): void
}>()

const refinedSchema = ScalePlanUpdateSchema.superRefine((data, ctx) => {
  const nextValue = data.value ?? scalePlan.value
  const nextTarget = data.targetPrice ?? scalePlan.targetPrice

  const otherTotal = trade.scalePlans
    .filter((plan) => plan.id !== scalePlan.id)
    .reduce((total, plan) => total + plan.value, 0)

  const newTotal = otherTotal + (nextValue ?? 0)
  if (newTotal > trade.positionSize) {
    ctx.addIssue({
      code: z.ZodIssueCode.custom,
      path: ['value'],
      message: `Total planned value (${newTotal.toFixed(2)}) exceeds position size (${trade.positionSize.toFixed(2)}).`,
    })
  }

  //TODO: account for short positions
  if (typeof nextTarget === 'number' && typeof trade.entryPriceAvg === 'number') {
    if (nextTarget < trade.entryPriceAvg) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        path: ['targetPrice'],
        message: `Target price must be ≥ entry price (${trade.entryPriceAvg.toFixed(2)}).`,
      })
    }
  }
})

const formSchema = toTypedSchema(refinedSchema)
const { updateMutation } = useScalePlanMutationService()
const { isSubmitting, handleSubmit, meta } = useForm({
  validationSchema: formSchema,
  initialValues: {
    ...scalePlan,
    stopPrice: undefined,
    limitPrice: undefined,
    goodTillDate: undefined,
  },
})

const onSubmit = handleSubmit(async (values) => {
  updateMutation.mutate(
    {
      id: scalePlan.id,
      data: values,
    },
    {
      onSuccess: () => {
        $emit('close')
      },
    },
  )
})
</script>

<template>
  <p class="text-xs font-semibold text-center mb-3">Scale plan for {{ scalePlan.label }}</p>
  <form class="flex flex-col h-full relative" :validation-schema="formSchema" @submit="onSubmit">
    <FormLoadingSpinner :isSubmitting="isSubmitting" />

    <div class="grid grid-cols-1 gap-3 md:grid-cols-12">
      <ScalePlanFormFields />
    </div>
    <Button type="submit" class="mt-3" :disabled="isSubmitting || !meta.dirty">
      Edit {{ scalePlan.label }} Scale Plan
    </Button>
  </form>
</template>
