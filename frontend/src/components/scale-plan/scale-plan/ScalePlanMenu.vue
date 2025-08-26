<script lang="ts" setup>
import { Icon } from '@iconify/vue'
import { useScalePlanMutations } from '@/composables'
import type { ScalePlan } from '@/interfaces'
const { deletePlanMutation } = useScalePlanMutations()
defineProps<{
  idx: number
  plan: ScalePlan
}>()

const emit = defineEmits<{
  (e: 'open-form', type: 'execute' | 'edit'): []
}>()
const menuOpen = defineModel<boolean>('menu-open')
const confirmOpen = defineModel<boolean>('confirm-open')

const onConfirmDelete = async (planId: string) => {
  await deletePlanMutation.mutateAsync(planId, {
    onSettled() {
      menuOpen.value = false
      confirmOpen.value = false
    },
  })
}
</script>

<template>
  <DropdownMenu
    as-child
    :open="menuOpen || confirmOpen"
    @update:open="
      (v: boolean) => {
        menuOpen = v
      }
    "
  >
    <DropdownMenuTrigger class="absolute top-1 right-1">
      <Button
        variant="ghost"
        size="sm"
        aria-label="Open trade menu"
        aria-haspopup="menu"
        class="h-11 w-11 p-0 rounded-full min-w-[44px] min-h-[44px] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2"
      >
        ⋯
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent side="bottom" align="end" :avoidCollisions="false">
      <DropdownMenuItem @select="emit('open-form', 'execute')">
        <Icon icon="lucide:circle-fading-arrow-up" width="24" height="24" />Execute Plan
      </DropdownMenuItem>
      <DropdownMenuItem @select="emit('open-form', 'edit')">
        <Icon icon="lucide:edit" width="24" height="24" />edit
      </DropdownMenuItem>
      <AlertDialog
        :open="confirmOpen"
        @update:open="
          (v: boolean) => {
            confirmOpen = v
          }
        "
      >
        <AlertDialogTrigger as-child>
          <DropdownMenuItem
            :hidden="plan.status !== 'planned'"
            class="text-red-600"
            @click.stop="confirmOpen = true"
            ><Icon icon="lucide:trash-2" width="24" height="24" />
            Delete Plan
          </DropdownMenuItem>
        </AlertDialogTrigger>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle
              >Delete {{ plan.label?.trim() || `Plan T${idx + 1}` }}?</AlertDialogTitle
            >
            <AlertDialogDescription>
              This action cannot be undone. This will permanently remove this scale plan from the
              trade.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel @click="confirmOpen = false">Cancel</AlertDialogCancel>
            <AlertDialogAction
              class="bg-red-600 hover:bg-red-700 text-white"
              @click="onConfirmDelete(plan.id)"
            >
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
