<script lang="ts" setup>
import { Icon } from '@iconify/vue'
import { type FieldEntry } from 'vee-validate'
import type { ScalePlanCreate } from '@/interfaces'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/tabs'
import TargetPlanForm from './TargetPlanForm.vue'

const props = defineProps<{
  targetPlans: FieldEntry<ScalePlanCreate>[]
}>()

const emit = defineEmits<{
  (e: 'add-target'): void
  (e: 'remove-plan', plan: FieldEntry<ScalePlanCreate>): void
}>()

const activeTab = ref('0')

// Watch for changes in target plans to handle tab management
watch(
  () => props.targetPlans.length,
  (newLength, oldLength) => {
    // If we removed a tab and the active tab is now out of bounds, adjust it
    const currentIndex = parseInt(activeTab.value)
    if (newLength < oldLength && currentIndex >= newLength) {
      activeTab.value = Math.max(0, newLength - 1).toString()
    }
    // If we added a new tab, switch to it
    if (newLength > oldLength) {
      activeTab.value = (newLength - 1).toString()
    }
  },
)

const handleRemovePlan = (plan: FieldEntry<ScalePlanCreate>) => {
  emit('remove-plan', plan)
}
</script>

<template>
  <div class="space-y-4">
    <!-- Empty State -->
    <div v-if="targetPlans.length === 0" class="text-slate-500 text-sm text-center py-8">
      <div class="flex flex-col items-center gap-2">
        <Icon icon="lucide:target" width="32" height="32" class="text-slate-600" />
        <p class="font-medium">No target plans yet</p>
        <p>Click "Add Target" to create exit strategies</p>
      </div>
    </div>

    <!-- Tabs Interface -->
    <Tabs v-else v-model="activeTab" class="w-full">
      <TabsList
        class="grid w-full bg-slate-800/50 border border-slate-600"
        :style="{ gridTemplateColumns: `repeat(${targetPlans.length}, minmax(0, 1fr))` }"
      >
        <TabsTrigger
          v-for="(plan, index) in targetPlans"
          :key="plan.key"
          :value="index.toString()"
          class="flex items-center gap-2 data-[state=active]:bg-blue-600 data-[state=active]:text-white text-slate-300 hover:text-white"
        >
          <Icon icon="lucide:target" width="16" height="16" />
          Target {{ index + 1 }}
        </TabsTrigger>
      </TabsList>

      <TabsContent
        v-for="(plan, index) in targetPlans"
        :key="plan.key"
        :value="index.toString()"
        class="bg-slate-800/30 rounded-lg p-4 mt-4"
      >
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-sm font-medium text-slate-200 flex items-center gap-2">
            <Icon icon="lucide:target" width="16" height="16" class="text-blue-400" />
            Target {{ index + 1 }} Details
          </h3>
          <Button
            variant="ghost"
            size="sm"
            class="text-red-400 hover:text-red-300 hover:bg-red-900/20"
            @click.prevent="handleRemovePlan(plan)"
          >
            <Icon icon="lucide:trash-2" width="16" height="16" />
          </Button>
        </div>

        <TargetPlanForm :key="plan.key" :idx="plan.key" @remove-plan="handleRemovePlan(plan)" />
      </TabsContent>
    </Tabs>
  </div>
</template>
