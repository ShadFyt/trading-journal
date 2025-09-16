<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { Tooltip } from '@/components/ui/tooltip'
import { toTypedSchema } from '@vee-validate/zod'
import { ScalePlanCreateSchema } from '@/schemas'
import { useForm } from 'vee-validate'
import { useInjectTradeMetrics, useScalePlanMutations } from '@/composables'
import { OrderTypeEnum, ScalePlanTypeEnum } from '@/enums'
import { addScalePlanLimitIssue, addScalePlanTargetPriceIssue } from '@/utils/scale-plan.util.ts'

const { initialPosition, trade, entryPlan } = useInjectTradeMetrics()

const targetPlans = computed(() =>
  trade.value.scalePlans.filter((p) => p.planType === ScalePlanTypeEnum.enum.TARGET),
)
const isDisabled = computed(() => {
  const totalQty = targetPlans.value.reduce((sum, p) => sum + (p.qty ?? 0), 0)
  return totalQty >= initialPosition
})

const open = ref(false)

const refinedSchema = ScalePlanCreateSchema.superRefine((data, ctx) => {
  const existingTotal = targetPlans.value.reduce((sum, p) => sum + (p.qty ?? 0), 0)
  const newTotal = existingTotal + (data.qty ?? 0)
  addScalePlanLimitIssue(ctx, initialPosition, newTotal)
  addScalePlanTargetPriceIssue(ctx, data.targetPrice, entryPlan.value.entryPriceAvg)
})

const formSchema = toTypedSchema(refinedSchema)
const { createPlanMutation } = useScalePlanMutations()
const { isSubmitting, handleSubmit, meta } = useForm({
  validationSchema: formSchema,
  initialValues: {
    notes: '',
    orderType: OrderTypeEnum.enum.LIMIT,
    planType: ScalePlanTypeEnum.enum.TARGET,
    targetPrice: entryPlan.value.entryPriceAvg + 0.5,
    label: `T${targetPlans.value.length + 1}(Target ${targetPlans.value.length + 1})`,
    tradeType: entryPlan.value.tradeType,
  },
})

const onSubmit = handleSubmit(async (values) => {
  createPlanMutation.mutate(
    {
      data: values,
      tradeId: trade.value.id,
    },
    {
      onSuccess() {
        open.value = false
      },
    },
  )
})
</script>

<template>
  <Popover v-model:open="open">
    <PopoverTrigger
      :disabled="isDisabled"
      :class="isDisabled ? 'opacity-50 cursor-not-allowed' : ''"
    >
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger as-child disabled>
            <Icon
              :class="
                isDisabled ? 'opacity-50 cursor-not-allowed' : 'hover:opacity-80 cursor-pointer'
              "
              icon="lucide:battery-plus"
              width="24"
              height="24"
            />
          </TooltipTrigger>
          <TooltipContent>
            <p class="text-xs font-semibold tracking-wide">
              {{ isDisabled ? 'Max quantity reached' : 'Add Target Plan' }}
            </p>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    </PopoverTrigger>
    <PopoverContent class="p-0 bg-slate-900 rounded-lg">
      <Card class="border border-slate-600 rounded-lg p-4 bg-slate-800/50 border-none">
        <form
          class="flex flex-col h-full relative m-0 p-0"
          :validation-schema="formSchema"
          @submit="onSubmit"
        >
          <FormLoadingSpinner :isSubmitting="isSubmitting" />
          <CardHeader class="bg-blue-900/30 flex justify-between px-4 py-3 -m-4 mb-4 rounded-t-lg">
            <CardTitle class="text-blue-400 text-base flex gap-2">
              <Icon icon="lucide:target" width="24" height="24" /> Add Plan
            </CardTitle>
            <Button type="submit" size="sm" class="gap-1" :disabled="!meta.valid || isSubmitting">
              <Icon icon="lucide:plus" width="24" height="24" /> Add Target
            </Button>
          </CardHeader>
          <CardContent class="space-y-4 p-0">
            <div class="grid grid-cols-1 sm:grid-cols-12 gap-4 items-start">
              <ScalePlanFormFields />
            </div>
          </CardContent>
        </form>
      </Card>
    </PopoverContent>
  </Popover>
</template>
