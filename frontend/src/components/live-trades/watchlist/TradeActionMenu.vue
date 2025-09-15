<script lang="ts" setup>
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Icon } from '@iconify/vue'
import type { Trade } from '@/interfaces'
import { useInjectTradeActions, useTradeMutationService } from '@/composables'

const { trade } = defineProps<{ trade: Trade }>()

const tradeActions = useInjectTradeActions()
const { invalidateMutation } = useTradeMutationService()

const handleInvalidate = () => {
  invalidateMutation.mutate(trade.id, { onSuccess: () => tradeActions.clearSelectedTrade() })
}
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger
      class="h-8 w-8 p-0 rounded-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 hover:bg-gray-400"
    >
      ...
    </DropdownMenuTrigger>
    <DropdownMenuContent side="bottom" align="end" :avoidCollisions="false" class="bg-slate-900">
      <DropdownMenuItem @click="tradeActions.openExecutionForm">
        <Icon icon="lucide:circle-fading-plus" class="text-green-200" />Execute
      </DropdownMenuItem>
      <DropdownMenuItem @click="tradeActions.openTradeForm">
        <Icon icon="lucide:lightbulb" class="text-amber-200" />Edit Idea
      </DropdownMenuItem>
      <DropdownMenuItem class="text-red-600" @click="handleInvalidate">
        <Icon icon="lucide:octagon-x" class="text-red-400" />Invalidate
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
