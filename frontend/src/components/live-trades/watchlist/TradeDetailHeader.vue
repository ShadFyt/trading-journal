<script lang="ts" setup>
import { Icon } from '@iconify/vue'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import type { Trade } from '@/interfaces'
import { useInjectTradeActions } from '@/composables'

defineProps<{ trade: Trade }>()

const tradeActions = useInjectTradeActions()
</script>

<template>
  <CardHeader class="flex items-center justify-between flex-shrink-0">
    <h3 class="text-white font-semibold text-sm">{{ trade?.symbol }} Details</h3>
    <div>
      <DropdownMenu>
        <DropdownMenuTrigger>
          <Button
            variant="ghost"
            size="sm"
            aria-label="Open trade menu"
            aria-haspopup="menu"
            class="h-11 w-11 min-w-[44px] min-h-[44px] p-0 rounded-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 hover:bg-gray-400"
          >
            ⋯
          </Button>
        </DropdownMenuTrigger>
        <DropdownMenuContent
          side="bottom"
          align="end"
          :avoidCollisions="false"
          class="bg-slate-900"
        >
          <DropdownMenuItem @click="tradeActions.openExecutionForm">
            <Icon icon="lucide:circle-fading-plus" class="text-green-200" />Execute
          </DropdownMenuItem>
          <DropdownMenuItem @click="tradeActions.openTradeForm">
            <Icon icon="lucide:lightbulb" class="text-amber-200" />Edit Idea
          </DropdownMenuItem>
          <DropdownMenuItem class="text-red-600"
            ><Icon icon="lucide:octagon-x" class="text-red-400" />Invalidate
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
  </CardHeader>
</template>
