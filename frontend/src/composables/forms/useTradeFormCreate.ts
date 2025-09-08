import { useLiveTradeMutationService } from '@/composables'
import { tradeCreateSchema } from '@/schemas'
import { toTypedSchema } from '@vee-validate/zod'
import { useForm } from 'vee-validate'
import type { ScalePlanCreate } from '@/interfaces'
import { OrderTypeEnum, ScalePlanTypeEnum } from '@/enums'

export const useTradeFormCreate = (close?: (v: boolean) => void) => {
  const { createMutation } = useLiveTradeMutationService()
  const tradeFormSchema = toTypedSchema(tradeCreateSchema)

  const entryPlanFactory = (): ScalePlanCreate => ({
    orderType: OrderTypeEnum.enum.LIMIT,
    label: 'Entry',
    qty: 0,
    targetPrice: 0,
    notes: '',
    stopPrice: 0,
    limitPrice: 0,
    planType: ScalePlanTypeEnum.enum.ENTRY,
  })
  const getInitialValues = () => {
    return {
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

  const isFormValid = computed(() => tradeCreateSchema.safeParse(values).success)

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
