import { toTypedSchema } from '@vee-validate/zod'
import { tradeIdeaCreateSchema, tradeIdeaUpdateSchema } from '@/schemas'
import type { TradeIdea } from '@/interfaces/trade-idea.type'
import { useTradeIdeaMutationService } from '@/composables'
import { useForm } from 'vee-validate'

export const useTradeIdeaForm = (
  selectedTrade?: TradeIdea | null,
  close?: (v: boolean) => void,
) => {
  const { createMutation, updateMutation } = useTradeIdeaMutationService()
  const isEditMode = computed(() => Boolean(selectedTrade))
  const tradeIdeaFormSchema = toTypedSchema(
    isEditMode.value ? tradeIdeaUpdateSchema : tradeIdeaCreateSchema,
  )
  const getInitialValues = () => {
    const baseValues = {
      targetPrices: [] as number[],
      symbol: '',
      setup: '',
      rating: 1,
      entryMin: 0,
      entryMax: 0,
      stop: 0,
      catalysts: '',
      notes: '',
    }

    // If editing, merge with existing trade data
    return isEditMode.value && selectedTrade ? { ...baseValues, ...selectedTrade } : baseValues
  }

  const { isFieldDirty, handleSubmit, setFieldValue, isSubmitting } = useForm({
    validationSchema: tradeIdeaFormSchema,
    initialValues: getInitialValues(),
  })

  const onSubmit = handleSubmit(async (values) => {
    try {
      if (isEditMode.value && selectedTrade) {
        // Update existing trade
        await updateMutation.mutateAsync({
          id: selectedTrade.id,
          data: tradeIdeaUpdateSchema.parse(values),
        })
        close?.(false)
      } else {
        // Create new trade
        await createMutation.mutateAsync(tradeIdeaCreateSchema.parse(values))
      }
    } catch (error) {
      console.error('Form submission error:', error)
    }
  })

  return {
    isEditMode,
    isFieldDirty,
    setFieldValue,
    isSubmitting,
    onSubmit,
    schema: tradeIdeaFormSchema,
  }
}
