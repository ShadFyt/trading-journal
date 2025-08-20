<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { ScalePlanUpdateSchema } from '@/schemas'
import { useForm } from 'vee-validate'
import { useScalePlanMutationService } from '@/composables'
import type { ScalePlan } from '@/interfaces'

const { scalePlan } = defineProps<{
  scalePlan: ScalePlan
}>()

const $emit = defineEmits<{
  (e: 'close'): void
}>()

const formSchema = toTypedSchema(ScalePlanUpdateSchema)
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
  try {
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
  } catch (error) {
    console.error(error)
  }
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
