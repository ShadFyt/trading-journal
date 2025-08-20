<script setup lang="ts">
import { Icon } from '@iconify/vue'
import { Tooltip } from '@/components/ui/tooltip'
import { toTypedSchema } from '@vee-validate/zod'
import { ScalePlanCreateSchema } from '@/schemas'
import { useForm } from 'vee-validate'
import { useScalePlanMutationService } from '@/composables'
import type { LiveTrade } from '@/interfaces'
import { OrderTypeEnum, ScalePlanKindEnum } from '@/enums'

const props = defineProps<{
  trade: LiveTrade
}>()
const open = ref(false)

const formSchema = toTypedSchema(ScalePlanCreateSchema)
const { createMutation } = useScalePlanMutationService()
const { isFieldDirty, isSubmitting, handleSubmit } = useForm({
  validationSchema: formSchema,
  initialValues: {
    orderType: OrderTypeEnum.enum.LIMIT,
    kind: ScalePlanKindEnum.enum.SHARES,
  },
})

const onSubmit = handleSubmit(async (values) => {
  try {
    createMutation.mutate(
      {
        data: values,
        liveTradeId: props.trade.id,
      },
      {
        onSuccess() {
          open.value = false
        },
      },
    )
  } catch (error) {
    console.error(error)
  }
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
