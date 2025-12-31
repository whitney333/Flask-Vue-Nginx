<script setup>
import { AudioLines, ExternalLink, Eye, Heart, MessageCircle, Star, Coins } from 'lucide-vue-next'
import { ref, computed } from 'vue'

const { post } = defineProps({
  post: Object
})

const showMore = ref(false)

// trim down title
const title = computed(() => {
  if (!post?.title) return '-'
  return post.title.length > 25
    ? post.title.slice(0, 25) + '...'
    : post.title
})

// convert date to yyyy-mm-dd
const uploadDate = computed(() => {
  if (!post?.upload_date) return '-'
  return new Date(post.upload_date).toISOString().split('T')[0]
})

// redirect Bilibili
const handleVisit = () => {
  window.open(`https://www.bilibili.com/video/${post.bvid}`, '_blank')
}

// convert http to https
const imageUrl = computed(() => {
  if (!post?.image) return ''
  return post.image.replace(/^http:/, 'https:')
})
</script>

<template>
  <div class="w-full max-w-sm bg-white border border-gray-200 rounded-xl shadow flex flex-col overflow-hidden">

    <!-- Thumbnail -->
    <img :src="imageUrl" alt="thumbnail" class="w-full h-48 object-cover" />

    <!-- content -->
    <div class="p-4 flex flex-col justify-between flex-1">

      <!-- title -->
      <p class="text-sm font-medium text-gray-900 mb-2">{{ title }}</p>

      <!-- statistics -->
      <div class="flex flex-wrap gap-4 text-gray-600 text-sm mb-2">
        <div class="relative flex items-center gap-1 group" title="Likes">
          <Heart class="w-4 h-4"/>
          <span>{{ post.like }}</span>
          <!-- Tooltip -->
          <span
              class="absolute bottom-full mb-1 left-1/2 transform -translate-x-1/2
           bg-gray-700 text-white text-xs px-2 py-1 rounded opacity-0
           group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
            Likes
          </span>
        </div>
        <div class="relative flex items-center gap-1 group" title="Comments">
          <MessageCircle class="w-4 h-4"/>
          <span>{{ post.comment }}</span>
          <!-- Tooltip -->
          <span
              class="absolute bottom-full mb-1 left-1/2 transform -translate-x-1/2
           bg-gray-700 text-white text-xs px-2 py-1 rounded opacity-0
           group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
            Comments
          </span>
        </div>
        <div class="relative flex items-center gap-1 group" title="Danmu">
          <AudioLines class="w-4 h-4"/>
          <span>{{ post.danmu }}</span>
          <!-- Tooltip -->
            <span
                class="absolute bottom-full mb-1 left-1/2 transform -translate-x-1/2
             bg-gray-700 text-white text-xs px-2 py-1 rounded opacity-0
             group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
              Danmaku
            </span>
        </div>
        <div class="relative flex items-center gap-1 group" title="Views">
          <Eye class="w-4 h-4"/>
          <span>{{ post.view }}</span>
          <!-- Tooltip -->
          <span
              class="absolute bottom-full mb-1 left-1/2 transform -translate-x-1/2
           bg-gray-700 text-white text-xs px-2 py-1 rounded opacity-0
           group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
            Views
          </span>
        </div>
        <div class="relative flex items-center gap-1 group" title="Collects">
          <Star class="w-4 h-4"/>
          <span>{{ post.collect }}</span>
          <!-- Tooltip -->
          <span
              class="absolute bottom-full mb-1 left-1/2 transform -translate-x-1/2
           bg-gray-700 text-white text-xs px-2 py-1 rounded opacity-0
           group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
            Collections
          </span>
        </div>
        <div class="relative flex items-center gap-1 group" title="Coins">
          <Coins class="w-4 h-4"/>
          <span>{{ post.coin }}</span>
          <!-- Tooltip -->
          <span
              class="absolute bottom-full mb-1 left-1/2 transform -translate-x-1/2
           bg-gray-700 text-white text-xs px-2 py-1 rounded opacity-0
           group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
            Coins
          </span>
        </div>
        <div class="relative flex items-center gap-1 group" title="Shares">
          <ExternalLink class="w-4 h-4"/>
          <span>{{ post.share }}</span>
          <!-- Tooltip -->
          <span
              class="absolute bottom-full mb-1 left-1/2 transform -translate-x-1/2
           bg-gray-700 text-white text-xs px-2 py-1 rounded opacity-0
           group-hover:opacity-100 transition-opacity whitespace-nowrap z-10">
            Shares
          </span>
        </div>
      </div>

      <!-- bottom -->
      <div class="flex justify-between items-center text-xs text-gray-500">
        <span>{{ uploadDate }}</span>
        <v-btn color="secondary" icon="mdi-chevron-right" size="small" @click="handleVisit"/>
      </div>

    </div>
  </div>
</template>

<style scoped>

</style>