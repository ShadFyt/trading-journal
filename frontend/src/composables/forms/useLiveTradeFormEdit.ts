import { useTradeMutationService } from '@/composables'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import type { Trade, TradeUpdate } from '@/interfaces/trade.type.ts'
import { LiveTradeUpdateSchema } from '@/schemas'
import { useFormatters } from '@/composables'

export const useLiveTradeFormEdit = (
  trade: Trade,
  formType: 'edit' | 'close',
  close?: (v: boolean) => void,
) => {
  const { convertStringToDate } = useFormatters()
  const { updateMutation, deleteMutation } = useTradeMutationService()
  const liveTradeFormSchema = toTypedSchema(LiveTradeUpdateSchema)

  const getInitialValues = () => {
    const { annotations, exitDate, enterDate, outcome, exitPriceAvg, ...rest } = trade
    return {
      ...rest,
      exitDate: exitDate ? convertStringToDate(exitDate) : undefined,
      enterDate: convertStringToDate(enterDate),
      outcome: outcome ?? 'pending',
      exitPriceAvg: exitPriceAvg ?? undefined,
    }
  }

  const { isFieldDirty, handleSubmit, setFieldValue, isSubmitting, meta } = useForm<TradeUpdate>({
    validationSchema: liveTradeFormSchema,
    initialValues: getInitialValues(),
  })

  const onSubmit = handleSubmit(async (values) => {
    try {
      const message = formType === 'close' ? 'successfully closed trade' : undefined
      await updateMutation.mutateAsync({ id: trade.id, data: values, message })
      close?.(false)
    } catch (error) {
      console.error('Form submission error:', error)
      throw error
    }
  })

  const onDelete = () => {
    try {
      deleteMutation.mutate(trade.id)
      close?.(false)
    } catch (error) {
      console.error('Delete error:', error)
      throw error
    }
  }

  return {
    isFieldDirty,
    onSubmit,
    setFieldValue,
    isSubmitting,
    meta,
    schema: liveTradeFormSchema,
    onDelete,
  }
}
