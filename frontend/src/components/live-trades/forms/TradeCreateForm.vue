<script lang="ts" setup>
import { Icon } from '@iconify/vue'
import { useTradeFormCreate } from '@/composables'
import { ScalePlanTypeEnum } from '@/enums'
const { onSubmit, isFormValid, schema, setFieldValue, isFieldDirty, trade } = useTradeFormCreate()
const entryPlan = computed(() =>
  trade.scalePlans?.find((p) => p.planType === ScalePlanTypeEnum.enum.ENTRY),
)
</script>

<template>
  <form :validation-schema="schema" class="h-screen w-96 flex flex-col">
    <header class="p-4 border-b border-slate-700 flex items-center justify-between">
      <h2 class="text-lg font-semibold">New Trade Idea</h2>
      <div class="flex gap-2">
        <Button variant="ghost" class="text-slate-400 hover:text-white" @click="$emit('cancel')">
          Cancel
        </Button>
        <Button :disabled="!isFormValid" class="gap-1" @click="onSubmit">
          <Icon icon="lucide:check" width="24" height="24" /> Save Trade
        </Button>
      </div>
    </header>

    <section class="flex-1 overflow-y-auto">
      <Card class="border-none bg-slate-900/60">
        <CardHeader>
          <CardTitle class="text-base text-slate-100">Basic Details</CardTitle>
        </CardHeader>
        <CardContent class="space-y-4">
          <BasicTradeField :set-field-value="setFieldValue" :is-field-dirty="isFieldDirty" />
          <PlanForm v-if="entryPlan" :plan="entryPlan" :is-entry="true" />
        </CardContent>
      </Card>
    </section>
  </form>
</template>
