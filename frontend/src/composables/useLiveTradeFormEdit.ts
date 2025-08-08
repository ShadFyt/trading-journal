import { useLiveTradeMutationService } from './useLiveTradeService'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import type { LiveTrade } from '@/interfaces/live-trade.type'
import { LiveTradeUpdateSchema } from '@/schemas'

export const useLiveTradeFormEdit = (trade: LiveTrade) => {
  const { updateMutation } = useLiveTradeMutationService()
  const liveTradeFormSchema = toTypedSchema(LiveTradeUpdateSchema)

  const getInitialValues = () => {
    const { annotations, ...rest } = trade
    return {
      ...rest,
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
