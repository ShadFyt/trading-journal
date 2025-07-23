<script lang="ts" setup>
import { Icon } from '@iconify/vue'

import { statusOptions } from '@/shared/status'
const statusFilter = defineModel('statusFilter', { type: String })
const searchQuery = defineModel('searchQuery', { type: String })
</script>

<template>
  <header class="flex justify-between items-center mb-6">
    <h1 class="text-3xl font-extrabold tracking-tight text-blue-800 drop-shadow-sm">
      Swing Trading Watchlist
    </h1>
    <div class="flex gap-2">
      <div class="relative flex-grow max-w-md">
        <Input
          v-model="searchQuery"
          type="text"
          placeholder="Search Trade Ideas..."
          class="w-full pl-10 pr-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
        <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
          <Icon icon="lucide:search" width="20" height="20" class="text-gray-400" />
        </div>
      </div>
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
    </div>
  </header>
</template>
