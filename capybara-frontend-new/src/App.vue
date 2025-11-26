<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
    <NavBar />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import NavBar from './components/NavBar.vue'
</script>