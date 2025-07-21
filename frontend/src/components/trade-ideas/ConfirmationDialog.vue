<script setup lang="ts">
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import { useTradeIdeaMutationService } from '@/composables'
import type { TradeIdea } from '@/interfaces/trade-idea.type'
const { deleteMutation } = useTradeIdeaMutationService()

defineProps<{ open: boolean; selectedTrade: TradeIdea }>()
const emit = defineEmits<{ (e: 'close'): void }>()
const handleDelete = (id: string) => {
  deleteMutation.mutate(id, {
    onSuccess: () => {
      emit('close')
    },
  })
}
</script>

<template>
  <AlertDialog :open="open">
    <AlertDialogContent>
      <AlertDialogHeader>
        <AlertDialogTitle
          >Are you absolutely sure you wish to delete trade idea for
          {{ selectedTrade.symbol }}?</AlertDialogTitle
        >
        <AlertDialogDescription>
          This action cannot be undone. This will permanently delete your trade idea and remove your
          data from our servers.
        </AlertDialogDescription>
      </AlertDialogHeader>
      <AlertDialogFooter>
        <AlertDialogCancel @click="emit('close')">Cancel</AlertDialogCancel>
        <AlertDialogAction @click="handleDelete(selectedTrade.id)">Delete</AlertDialogAction>
      </AlertDialogFooter>
    </AlertDialogContent>
  </AlertDialog>
</template>
