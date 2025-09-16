<script lang="ts" setup>
import type { Trade } from '@/interfaces'

defineProps<{ trade: Trade }>()
</script>

<template>
  <Avatar>
    <AvatarImage :src="trade?.logo ?? ''" :alt="trade.symbol" />
    <AvatarFallback>{{ trade.symbol.slice(0, 2).toUpperCase() }}</AvatarFallback>
  </Avatar>
</template>
