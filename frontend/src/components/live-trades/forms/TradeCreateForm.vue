<script lang="ts" setup>
import { Icon } from '@iconify/vue'
import { useTradeFormCreate } from '@/composables'
import { ScalePlanTypeEnum } from '@/enums'
import { targetPlanFactory } from '@/utils'
const { onSubmit, isFormValid, schema, setFieldValue, isFieldDirty, trade } = useTradeFormCreate()

const entryPlan = computed(() =>
  trade.scalePlans?.find((p) => p.planType === ScalePlanTypeEnum.enum.ENTRY),
)
const targetPlans = computed(
  () => trade?.scalePlans?.filter((p) => p.planType === ScalePlanTypeEnum.enum.TARGET) ?? [],
)

const addTargetPlan = () => {
  const idx = targetPlans.value.length + 1
  setFieldValue('scalePlans', [
    ...(trade?.scalePlans ?? []),
    targetPlanFactory(idx, entryPlan.value?.limitPrice),
  ])
}
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
        </CardContent>
      </Card>
      <Card class="border border-slate-600 rounded-lg p-4 bg-slate-800/50 m-2">
        <CardHeader class="flex items-center gap-2 bg-emerald-900 px-4 py-3 -m-4 mb-4 rounded-t-lg">
          <CardTitle class="text-base text-slate-100 flex text-center">
            <span class="font-medium text-md text-emerald-300">Entry Plan</span>
          </CardTitle>
        </CardHeader>
        <CardContent class="space-y-4 p-0">
          <EntryPlanForm />
        </CardContent>
      </Card>
      <Card class="border border-slate-600 rounded-lg p-4 bg-slate-800/50 m-2">
        <CardHeader
          class="bg-blue-900/30 flex justify-between gap-2 px-4 py-3 -m-4 mb-4 rounded-t-lg"
        >
          <CardTitle class="text-blue-400 text-base flex gap-2">
            <Icon icon="lucide:target" width="24" height="24" /> Target Plans
          </CardTitle>
          <Button size="sm" class="gap-1" @click.prevent="addTargetPlan">
            <Icon icon="lucide:plus" width="24" height="24" /> Add Target
          </Button>
        </CardHeader>
        <CardContent class="space-y-4 p-0">
          <div v-if="targetPlans.length === 0" class="text-slate-500 text-sm text-center py-8">
            <p>No target plans yet.</p>
            <p>Click "Add Target" to create exit strategies.</p>
          </div>
          <TargetPlanForm
            v-for="plan in targetPlans"
            :key="plan.targetPrice"
            :plan
            :is-entry="false"
          />
        </CardContent>
      </Card>
    </section>
  </form>
</template>
