<script setup>
  import { useCounterStore } from '@/stores/counter';
  import { ref } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  const instance = ref("")
  const router = useRouter()
  const route = useRoute()
  const counterStore = useCounterStore()
  const handleIncrement = () => {
    counterStore.increment()
  }
  const handleToAbout = () => {
    router.push({path: '/about'})
  }

</script>

<template>
  <div class="flex-row">
    <v-btn @click="handleToAbout">To About</v-btn>
    <v-btn @click="handleIncrement">{{ counterStore.count }}</v-btn>
    <template>{{ instance }}</template>
  </div>

</template>
