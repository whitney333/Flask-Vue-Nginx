<script setup>
defineProps({
  edit: {
    type: Boolean,
    default: false
  }
})
</script>

<template>
<v-chip :color="edit ? 'indigo' : 'grey'" text-color="white" size="small">
    {{ edit ? 'Edit Mode' : 'View Mode' }}
  </v-chip>
</template>

<style scoped>

</style>