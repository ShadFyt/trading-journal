<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { Tooltip } from '@/components/ui/tooltip'
import { toTypedSchema } from '@vee-validate/zod'
import { ScalePlanCreateSchema } from '@/schemas'
import { useForm } from 'vee-validate'
import { useScalePlanMutations, useTradeMetrics } from '@/composables'
import type { LiveTrade } from '@/interfaces'
import { OrderTypeEnum, ScalePlanTypeEnum } from '@/enums'
import { addScalePlanLimitIssue, addScalePlanTargetPriceIssue } from '@/utils/scale-plan.util.ts'

const { trade } = defineProps<{
  trade: LiveTrade
}>()
const { initialPosition, entryPrice } = useTradeMetrics(trade)

const open = ref(false)

const refinedSchema = ScalePlanCreateSchema.superRefine((data, ctx) => {
  // 1) Total value cap: sum(existing) + new.value <= positionSize
  const existingTotal = trade.scalePlans.reduce(
    (sum, p) => sum + (p.planType === ScalePlanTypeEnum.enum.TARGET ? p.qty : 0),
    0,
  )
  const newTotal = existingTotal + (data.qty ?? 0)
  addScalePlanLimitIssue(ctx, initialPosition, newTotal)
  addScalePlanTargetPriceIssue(ctx, data.targetPrice, entryPrice)
})

const formSchema = toTypedSchema(refinedSchema)
const { createPlanMutation } = useScalePlanMutations()
const { isFieldDirty, isSubmitting, handleSubmit } = useForm({
  validationSchema: formSchema,
  initialValues: {
    notes: '',
    orderType: OrderTypeEnum.enum.LIMIT,
    planType: ScalePlanTypeEnum.enum.TARGET,
    targetPrice: entryPrice + 0.5,
    label: `T${trade.scalePlans.length + 1}(Target ${trade.scalePlans.length + 1})`,
  },
})

const onSubmit = handleSubmit(async (values) => {
  createPlanMutation.mutate(
    {
      data: values,
      tradeId: trade.id,
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
    <PopoverTrigger>
      <TooltipProvider>
        <Tooltip>
          <TooltipTrigger as-child>
            <Icon
              class="hover:opacity-80 cursor-pointer"
              icon="lucide:battery-plus"
              width="24"
              height="24"
            />
          </TooltipTrigger>
          <TooltipContent>
            <p class="text-xs font-semibold tracking-wide">Add Scale Plan</p>
          </TooltipContent>
        </Tooltip>
      </TooltipProvider>
    </PopoverTrigger>
    <PopoverContent>
      <p class="text-xs font-semibold text-center mb-3">Scale Out Plan</p>
      <form
        class="flex flex-col h-full relative"
        :validation-schema="formSchema"
        @submit="onSubmit"
      >
        <FormLoadingSpinner :isSubmitting="isSubmitting" />

        <div class="grid grid-cols-1 gap-3 md:grid-cols-12">
          <ScalePlanFormFields />
        </div>
        <Button type="submit" class="mt-3" :disabled="!isFieldDirty('qty') || isSubmitting">
          Add New Plan
        </Button>
      </form>
    </PopoverContent>
  </Popover>
</template>
