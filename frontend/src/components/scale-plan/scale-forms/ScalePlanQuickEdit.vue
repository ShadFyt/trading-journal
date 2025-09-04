<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { ScalePlanUpdateSchema } from '@/schemas'
import { useForm } from 'vee-validate'
import { useScalePlanMutations, useTradeMetrics } from '@/composables'
import type { LiveTrade, ScalePlan } from '@/interfaces'
import { addScalePlanLimitIssue, addScalePlanTargetPriceIssue } from '@/utils/scale-plan.util.ts'

const { scalePlan, trade } = defineProps<{
  scalePlan: ScalePlan
  trade: LiveTrade
}>()

const $emit = defineEmits<{
  (e: 'close'): void
}>()
const { initialPosition, entryPrice } = useTradeMetrics(trade)

const refinedSchema = ScalePlanUpdateSchema.superRefine((data, ctx) => {
  const nextValue = data.qty ?? scalePlan.qty
  const nextTarget = data.targetPrice ?? scalePlan.targetPrice

  const otherTotal = trade.scalePlans
    .filter((plan) => plan.id !== scalePlan.id)
    .reduce((total, plan) => total + plan.qty, 0)

  const newTotal = otherTotal + (nextValue ?? 0)
  addScalePlanLimitIssue(ctx, initialPosition, newTotal)
  addScalePlanTargetPriceIssue(ctx, nextTarget, entryPrice)
})

const formSchema = toTypedSchema(refinedSchema)
const { updatePlanMutation } = useScalePlanMutations()
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
  updatePlanMutation.mutate(
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
