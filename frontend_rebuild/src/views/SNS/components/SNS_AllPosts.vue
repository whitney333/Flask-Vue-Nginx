<script setup>
    import axios from '@/axios';
    import { computed, onMounted, ref, watch } from 'vue';
    import SNS_TikTok_PostCard from '@/views/SNS/components/SNS_TikTok_PostCard.vue';
    import SNS_Insta_PostCard from '@/views/SNS/components/SNS_Insta_PostCard.vue';
    import SNS_Youtube_PostCard from '@/views/SNS/components/SNS_Youtube_PostCard.vue';
    import SNS_Bilibili_PostCard from '@/views/SNS/components/SNS_Bilibili_PostCard.vue';
    import {useArtistStore} from "@/stores/artist.js";

    const props = defineProps({
        platform: String,
    })
    const first = ref(1)
    const posts = ref([])
    const loading = ref(true)
    const artistStore = useArtistStore()

    const displayPosts = computed(() => {
            return posts.value.slice((first.value - 1) * 6, ((first.value - 1) * 6) + 6)
        }
    )

    const hasPosts = computed(() => posts.value.length > 0);
    const platformId = computed(() => {
      if (!artistStore.artist) return null;

      switch (props.platform) {
        case 'tiktok':
          return artistStore.artist.tiktok_id;
        case 'instagram':
          return artistStore.artist.instagram_id;
        case 'youtube':
          return artistStore.artist.youtube_id;
        case 'bilibili':
          return artistStore.artist.bilibili_id;
        default:
          return null;
      }
    });

    
    const fetchPosts = async () => {
      loading.value = true;
      posts.value = [];

      // if no platform account, does not request api
      if (!platformId.value) {
        loading.value = false;
        return;
      }
      try {
            const res = await axios.get(`/${props.platform}/v1/posts?artist_id=${artistStore.artistId}`)
            // console.log(res.data.data);
            
            posts.value = res.data?.data
        } catch(e) {
        posts.value = postsExample
        // console.error(e);
        console.log(posts.value);
      } finally {
        loading.value = false;
      }
    }

    watch(
        () => artistStore.artistId,
        (newMid) => {
          if (newMid) {
            fetchPosts()
          }
        },
        {immediate: true}
    )


</script>
<template>
  <v-container fluid class="bg-gray-100">

    <div v-if="loading" class="text-center text-caption text-grey my-4">
      {{ $t('Loading...') }}
    </div>

    <div v-else-if="!platformId || !hasPosts" class="text-center text-caption text-grey my-4">
      {{ $t('No posts/accounts found for this platform.') }}
    </div>

    <div v-else>
      <div class="px-4 pt-2 pb-4 min-w-0">
        <h2 class="text-lg sm:text-xl md:text-2xl font-semibold text-gray-800">
          {{ $t('All/Latest Posts') }}
        </h2>
      </div>
      <!-- 貼文卡片 -->
      <div class="flex justify-center items-stretch gap-4 sm:gap-6 md:gap-10 xl:gap-16 flex-wrap">

        <template v-if="props.platform === 'tiktok'">
          <SNS_TikTok_PostCard
            v-for="post in displayPosts"
            :key="`${post.url}_${first}`"
            :post="post"
          />
        </template>

        <template v-else-if="props.platform === 'youtube'">
          <SNS_Youtube_PostCard
            v-for="post in displayPosts"
            :key="`${post.url}_${first}`"
            :post="post"
          />
        </template>

        <template v-else-if="props.platform === 'instagram'">
          <SNS_Insta_PostCard
            v-for="post in displayPosts"
            :key="`${post.url}_${first}`"
            :post="post"
          />
        </template>

        <template v-else-if="props.platform === 'bilibili'">
          <SNS_Bilibili_PostCard
            v-for="post in displayPosts"
            :key="post.aid"
            :post="post"
          />
        </template>

      </div>

      <!-- 分頁 -->
      <div class="text-center mt-6 mb-3">

        <!-- Desktop -->
        <v-pagination
          v-if="$vuetify.display.mdAndUp"
          v-model="first"
          :length="Math.ceil(posts.length / 6)"
          :total-visible="6"
          rounded="circle"
        />

        <!-- Mobile -->
        <div v-else class="flex justify-center items-center gap-3">

          <v-btn
            icon
            @click="first = Math.max(1, first - 1)"
            :disabled="first === 1"
          >
            ‹
          </v-btn>

          <span class="text-sm text-gray-600">
            {{ first }} / {{ Math.ceil(posts.length / 6) }}
          </span>

          <v-btn
            icon
            @click="first = Math.min(Math.ceil(posts.length / 6), first + 1)"
            :disabled="first === Math.ceil(posts.length / 6)"
          >
            ›
          </v-btn>
        </div>
      </div>
    </div>
  </v-container>
</template>

<style>
    .custom-paginator {
    background-color: transparent !important;
    border: none !important;
    }

</style>