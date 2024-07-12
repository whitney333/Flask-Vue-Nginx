<script setup>
  import { useCounterStore } from '../stores/counter';
  const counterStore = useCounterStore()
</script>


<template>
  <div class="about">
    <h1>This is an about page {{ counterStore.doubleCount }}</h1>
  </div>
</template>

<style>
</style>
