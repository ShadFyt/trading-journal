import { useLiveTradeMutationService } from '@/composables'
import { tradeCreateSchema } from '@/schemas'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { entryPlanFactory } from '@/utils'

export const useTradeFormCreate = (close?: (v: boolean) => void) => {
  const { createMutation } = useLiveTradeMutationService()
  const tradeFormSchema = toTypedSchema(tradeCreateSchema)

  const getInitialValues = () => {
    return {
      rating: 5,
      scalePlans: [entryPlanFactory()],
    }
  }

  const { values, isFieldDirty, handleSubmit, setFieldValue, isSubmitting, meta } = useForm({
    validationSchema: tradeFormSchema,
    initialValues: getInitialValues(),
  })

  const onSubmit = handleSubmit(async (values) => {
    try {
      await createMutation.mutateAsync(values)
      close?.(false)
    } catch (error) {
      console.error('Form submission error:', error)
      throw error
    }
  })

  const isFormValid = computed(() => meta.value.valid)

  return {
    isFieldDirty,
    onSubmit,
    setFieldValue,
    isSubmitting,
    meta,
    schema: tradeFormSchema,
    isFormValid,
    trade: values,
  }
}
