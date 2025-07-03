<script setup lang="ts"></script>

<template>
  <div>
    <label for="symbol" class="block text-sm font-medium text-gray-700">Symbol</label>
    <input
      type="text"
      id="symbol"
      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
      placeholder="e.g. AAPL"
    />
  </div>
  <div>
    <label for="entry-price" class="block text-sm font-medium text-gray-700"> Entry Price </label>
    <input
      type="number"
      id="entry-price"
      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
      placeholder="e.g. 150.50"
      step="0.01"
    />
  </div>
  <div>
    <label for="target-price" class="block text-sm font-medium text-gray-700"> Target Price </label>
    <input
      type="number"
      id="target-price"
      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
      placeholder="e.g. 165.00"
      step="0.01"
    />
  </div>
  <div>
    <label for="notes" class="block text-sm font-medium text-gray-700">Notes</label>
    <textarea
      id="notes"
      rows="3"
      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
      placeholder="Add any additional notes or analysis..."
    ></textarea>
  </div>
</template>
