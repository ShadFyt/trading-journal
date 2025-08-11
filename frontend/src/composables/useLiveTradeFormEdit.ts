import { useLiveTradeMutationService } from './useLiveTradeService'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import type { LiveTrade } from '@/interfaces/live-trade.type'
import { LiveTradeUpdateSchema } from '@/schemas'
import { useFormatters } from './useFormatters'

export const useLiveTradeFormEdit = (trade: LiveTrade) => {
  const { convertStringToDate } = useFormatters()
  const { updateMutation } = useLiveTradeMutationService()
  const liveTradeFormSchema = toTypedSchema(LiveTradeUpdateSchema)

  const getInitialValues = () => {
    const { annotations, exitDate, enterDate, ...rest } = trade
    return {
      ...rest,
      exitDate: exitDate ? convertStringToDate(exitDate) : undefined,
      enterDate: convertStringToDate(enterDate),
    }
  }

  const { isFieldDirty, handleSubmit, setFieldValue, isSubmitting, meta } = useForm({
    validationSchema: liveTradeFormSchema,
    initialValues: getInitialValues(),
  })

  const onSubmit = handleSubmit(async (values) => {
    try {
      await updateMutation.mutateAsync({ id: trade.id, data: values })
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
