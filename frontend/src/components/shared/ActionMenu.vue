<script lang="ts" setup>
import { Icon } from '@iconify/vue'
defineProps<{ alertTitle: string; alertDescription: string; triggerText: string }>()
const emit = defineEmits<{
  (e: 'delete'): []
}>()
const menuOpen = defineModel<boolean>('menu-open')
const confirmOpen = defineModel<boolean>('confirm-open')
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
    class="bg-slate-900"
  >
    <DropdownMenuTrigger class="absolute top-1 right-1">
      <Button
        variant="ghost"
        size="sm"
        aria-label="Open trade menu"
        aria-haspopup="menu"
        class="min-w-[33px] min-h-[33px] p-0 rounded-full focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-600 focus-visible:ring-offset-2 hover:bg-gray-400"
      >
        <slot name="trigger">...</slot>
      </Button>
    </DropdownMenuTrigger>
    <DropdownMenuContent side="bottom" align="end" :avoidCollisions="false" class="bg-slate-900">
      <slot name="extra-actions" />
      <AlertDialog
        :open="confirmOpen"
        @update:open="
          (v: boolean) => {
            confirmOpen = v
          }
        "
      >
        <AlertDialogTrigger as-child>
          <DropdownMenuItem class="text-red-600" @click.stop="confirmOpen = true"
            ><Icon icon="lucide:trash-2" width="24" height="24" />
            {{ triggerText }}
          </DropdownMenuItem>
        </AlertDialogTrigger>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>{{ alertTitle }}</AlertDialogTitle>
            <AlertDialogDescription>
              {{ alertDescription }}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <slot name="dialog-content" />
          <AlertDialogFooter>
            <AlertDialogCancel @click="confirmOpen = false">Cancel</AlertDialogCancel>
            <AlertDialogAction
              class="bg-red-600 hover:bg-red-700 text-white"
              @click="emit('delete')"
            >
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </DropdownMenuContent>
  </DropdownMenu>
</template>
