import { useLiveTradeMutationService } from './useLiveTradeService'
import { liveTradeCreateSchema } from '@/schemas'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import type { TradeIdea } from '@/interfaces/trade-idea.type'

export const useLiveTradeForm = (tradeIdea: TradeIdea) => {
  const { createMutation } = useLiveTradeMutationService()
  const liveTradeFormSchema = toTypedSchema(liveTradeCreateSchema)

  const getInitialValues = () => {
    const { entryMin, entryMax, notes, catalysts, ideaDate, id, ...rest } = tradeIdea
    return {
      ...rest,
      entryPriceAvg: entryMin,
      notes: notes ? [notes] : [],
      catalysts: catalysts ? [catalysts] : [],
      tradeIdeaId: id,
    }
  }

  const { isFieldDirty, handleSubmit, setFieldValue, isSubmitting, meta } = useForm({
    validationSchema: liveTradeFormSchema,
    initialValues: getInitialValues(),
  })

  const onSubmit = handleSubmit(async (values) => {
    try {
      await createMutation.mutateAsync(values)
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
