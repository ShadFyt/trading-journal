<script setup lang="ts">
import { RouterView } from 'vue-router'
import { Toaster } from '@/components/ui/sonner'
</script>

<template>
  <Toaster />
  <RouterView />
</template>

<style scoped>
@keyframes fadein {
  from {
    opacity: 0;
    transform: translateY(20px);
  }

  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fadein {
  animation: fadein 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
