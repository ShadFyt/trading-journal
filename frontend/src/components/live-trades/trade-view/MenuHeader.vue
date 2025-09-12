<script lang="ts" setup>
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
import { Button } from '@/components/ui/button'
import type { Trade } from '@/interfaces'

defineProps<{ trade: Trade }>()

const emit = defineEmits<{
  'close-trade': []
  'edit-trade': []
}>()
</script>

<template>
  <DropdownMenu>
    <DropdownMenuTrigger class="absolute top-2 right-2">
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
    <DropdownMenuContent side="bottom" align="end" :avoidCollisions="false" class="bg-slate-900">
      <DropdownMenuItem @click="emit('edit-trade')"> Edit Trade </DropdownMenuItem>
      <DropdownMenuItem class="text-red-600" @click="emit('close-trade')">
        Close Trade
      </DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
