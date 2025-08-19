import { useLiveTradeMutationService } from '../useLiveTradeService.ts'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import type { LiveTrade, LiveTradeUpdate } from '@/interfaces/live-trade.type.ts'
import { LiveTradeUpdateSchema } from '@/schemas'
import { useFormatters } from '../useFormatters.ts'

export const useLiveTradeFormEdit = (
  trade: LiveTrade,
  formType: 'edit' | 'close',
  close?: (v: boolean) => void,
) => {
  const { convertStringToDate } = useFormatters()
  const { updateMutation, deleteMutation } = useLiveTradeMutationService()
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

  const { isFieldDirty, handleSubmit, setFieldValue, isSubmitting, meta } =
    useForm<LiveTradeUpdate>({
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
