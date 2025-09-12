import { useTradeMutationService } from '@/composables'
import { extendedTradeCreateSchema } from '@/schemas'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import { entryPlanFactory } from '@/utils'
import type { Trade } from '@/interfaces'

export const useTradeForm = (close?: () => void, trade?: Trade | null) => {
  const { createMutation, replaceMutation } = useTradeMutationService()
  const tradeFormSchema = toTypedSchema(extendedTradeCreateSchema)

  const getInitialValues = () => {
    if (trade) {
      return { ...trade }
    }
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
      if (trade) {
        await replaceMutation.mutateAsync({ id: trade.id, data: values })
      } else {
        await createMutation.mutateAsync(values)
      }
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
