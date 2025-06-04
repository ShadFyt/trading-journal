<script setup lang="ts">
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
    <div class="flex space-x-8 mb-8">
      <a href="https://vite.dev" target="_blank">
        <img src="/vite.svg" alt="Vite logo" class="h-24 p-6 transition-filter duration-300 hover:drop-shadow-[0_0_2em_#646cffaa]" />
      </a>
      <a href="https://vuejs.org/" target="_blank">
        <img src="./assets/vue.svg" alt="Vue logo" class="h-24 p-6 transition-filter duration-300 hover:drop-shadow-[0_0_2em_#42b883aa]" />
      </a>
    </div>
    <HelloWorld msg="Vite + Vue" />
  </div>
</template>


