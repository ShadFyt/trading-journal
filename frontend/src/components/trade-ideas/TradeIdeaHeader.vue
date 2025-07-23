<script lang="ts" setup>
import { statusOptions } from '@/shared/status'
defineModel('statusFilter', { type: String })
</script>

<template>
  <header class="flex justify-between items-center mb-6">
    <h1 class="text-3xl font-extrabold tracking-tight text-blue-800 drop-shadow-sm">
      Swing Trading Watchlist
    </h1>
    <Select
      v-model="statusFilter"
      class="w-56 shadow-md rounded-lg border-blue-200 border-2 focus:ring-2 focus:ring-blue-400"
    >
      <SelectTrigger>
        <SelectValue placeholder="Filter by Status" />
      </SelectTrigger>
      <SelectContent>
        <SelectItem v-for="option in statusOptions" :key="option.value" :value="option.value">
          {{ option.label }}
        </SelectItem>
      </SelectContent>
    </Select>
  </header>
</template>
