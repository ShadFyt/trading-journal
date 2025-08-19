import { useLiveTradeMutationService } from '../useLiveTradeService.ts'
import { liveTradeCreateSchema } from '@/schemas'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import type { TradeIdea } from '@/interfaces/trade-idea.type.ts'

export const useLiveTradeFormCreate = (tradeIdea: TradeIdea, close?: (v: boolean) => void) => {
  const { createMutation } = useLiveTradeMutationService()
  const liveTradeFormSchema = toTypedSchema(liveTradeCreateSchema)

  const getInitialValues = () => {
    const { entryMin, entryMax, notes, catalysts, ideaDate, id, ...rest } = tradeIdea
    return {
      ...rest,
      entryPriceAvg: entryMin,
      notes: '',
      catalysts: '',
      tradeIdeaId: id,
      scalePlans: [],
    }
  }

  const { isFieldDirty, handleSubmit, setFieldValue, isSubmitting, meta } = useForm({
    validationSchema: liveTradeFormSchema,
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

  return {
    isFieldDirty,
    onSubmit,
    setFieldValue,
    isSubmitting,
    meta,
    schema: liveTradeFormSchema,
  }
}
