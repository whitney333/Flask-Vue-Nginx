<script setup>

  import { Captions, CaptionsOff, CirclePlay, Cog, Eye, Heart, MessageCircle, Send, Settings, Star, Tag } from 'lucide-vue-next';
  import Button from 'primevue/button';
  import Card from 'primevue/card';
  import Image from 'primevue/image';
  import ScrollPanel from 'primevue/scrollpanel';
  import { ref } from 'vue';
  const { post } = defineProps({
    post: Object
  })
  const showMore = ref(false)
  const title_temp = post.title.split("#")[0] !== "" ? post.title.split("#")[0] : post.title
  const title = title_temp.length > 67 ? `${title_temp.slice(0, 67).split(' ').slice(0, -1).join(' ')}...` : title_temp
  const hashtags = post?.hashtags ? post?.hashtags?.slice(0,5)?.map((h) => `#${h}`)?.join(", ") : "-"


  const handleVisit = () => {
    window.open(post.url)
  }

  const handleShowMore = () => {
    showMore.value = !showMore.value
  }

</script>


<template>
    <div class="max-w-sm xl:w-2/5 w-96 xl:min-w-2/5 xl:max-w-full xl:h-96 xl:flex">
      <Image class="h-48 w-96 xl:h-auto xl:w-64 flex-none rounded-t xl:rounded-t-none xl:rounded-l text-center overflow-hidden" preview>
        <template #image>
          <img class="object-cover w-full h-full" :src="post.thumbnail" alt="image" />
        </template>
        <template #original="preview">
          <img class="object-cover w-full h-full" :src="post.thumbnail" alt="image" />
        </template>
      </Image>
      <div class="border-r border-b border-l -mt-2 xl:-mt-0 border-gray-300 xl:border-l-0 w-full xl:border-t xl:border-gray-300 shadow bg-white rounded-b xl:rounded-b-none xl:rounded-r p-4 flex flex-col justify-between leading-normal">
        <div class="mb-2 flex flex-col gap-3">
          <p>{{ title }}</p>
          <div class="flex">
            <div class="text-gray-700 flex gap-2 w-full">
              <Heart />
              <span>
                {{ post.like_count }}
              </span>
            </div>
            <div class="text-gray-700 flex gap-2 w-full">
              <MessageCircle />
              <span>
                {{ post.comment_count }}
              </span>
            </div>
          </div>
          <div class="flex">
            <div class="text-gray-700 flex gap-2 w-full">
              <Star />
              <span>
                {{ post.favorite_count }}
              </span>
            </div>
            <div class="text-gray-700 flex gap-2 w-full">
              <Eye />
              <span>
                {{ post.view_count }}
              </span>
            </div>
          </div>
          <div class="text-gray-700 text-sm flex gap-2 w-full items-center">
            <Settings />
            <span>{{ post.eng_rate }}</span>
          </div>
        </div>
        <div class="text-sm flex items-center gap-1">
          <div class="w-full">
            <p class="text-gray-600">{{ post?.upload_date?.$date.split("T")[0] }}</p>
          </div>
          <div class=" items-center gap-5 w-full flex justify-end">
            <Button icon="pi pi-angle-right" severity="primary" @click="handleVisit" raised />
          </div>
        </div>

    </div>
  </div>
</template>