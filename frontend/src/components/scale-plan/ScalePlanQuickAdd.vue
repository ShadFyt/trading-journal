<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { Tooltip } from '@/components/ui/tooltip'
import { toTypedSchema } from '@vee-validate/zod'
import { ScalePlanCreateSchema } from '@/schemas'
import { useForm } from 'vee-validate'
import { useScalePlanMutationService } from '@/composables'
import type { LiveTrade } from '@/interfaces'
import { OrderTypeEnum, ScalePlanKindEnum } from '@/enums'
import { addScalePlanLimitIssue, addScalePlanTargetPriceIssue } from '@/utils/scale-plan.util.ts'

const { trade } = defineProps<{
  trade: LiveTrade
}>()
const open = ref(false)

const refinedSchema = ScalePlanCreateSchema.superRefine((data, ctx) => {
  // 1) Total value cap: sum(existing) + new.value <= positionSize
  const existingTotal = trade.scalePlans.reduce((sum, p) => sum + (p.value ?? 0), 0)
  const newTotal = existingTotal + (data.value ?? 0)
  addScalePlanLimitIssue(ctx, trade.positionSize, newTotal, data.kind)
  addScalePlanTargetPriceIssue(ctx, data.targetPrice, trade.entryPriceAvg)
})

const formSchema = toTypedSchema(refinedSchema)
const { createMutation } = useScalePlanMutationService()
const { isFieldDirty, isSubmitting, handleSubmit } = useForm({
  validationSchema: formSchema,
  initialValues: {
    orderType: OrderTypeEnum.enum.LIMIT,
    kind: ScalePlanKindEnum.enum.SHARES,
    targetPrice: trade.entryPriceAvg + 0.5,
    label: `T${trade.scalePlans.length + 1}(Target ${trade.scalePlans.length + 1})`,
  },
})

const onSubmit = handleSubmit(async (values) => {
  createMutation.mutate(
    {
      data: values,
      liveTradeId: trade.id,
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
        <Button type="submit" class="mt-3" :disabled="!isFieldDirty('label') || isSubmitting">
          Add Scale Plan
        </Button>
      </form>
    </PopoverContent>
  </Popover>
</template>
