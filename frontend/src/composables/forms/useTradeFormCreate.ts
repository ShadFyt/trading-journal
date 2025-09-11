import { useLiveTradeMutationService } from '@/composables'
import { extendedTradeCreateSchema } from '@/schemas'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { entryPlanFactory } from '@/utils'

export const useTradeFormCreate = (close?: () => void) => {
  const { createMutation } = useLiveTradeMutationService()
  const tradeFormSchema = toTypedSchema(extendedTradeCreateSchema)

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
      close?.()
    } catch (error) {
      console.error('Form submission error:', error)
      throw error
    }
  })

  return {
    isFieldDirty,
    onSubmit,
    setFieldValue,
    isSubmitting,
    meta,
    schema: tradeFormSchema,
    trade: values,
  }
}
