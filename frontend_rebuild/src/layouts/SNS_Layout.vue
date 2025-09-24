<script setup>
  import { currentProfile } from '@/libs/current-profile';
  import { getAuth } from 'firebase/auth';
  import { useRouter } from 'vue-router';

  console.log("Running Layout...");

  // const router = useRouter()
  // const { currentUser } = getAuth()
  //
  // if (!currentUser) {
  //   router.push('/auth/login')
  // } else {
  //   const profile = await currentProfile()
  //
  //   if (!profile) {
  //     router.push('/auth/register/details')
  //   }
  //
  // }

</script>

<template>
  <router-view :profile="profile"></router-view>
</template>