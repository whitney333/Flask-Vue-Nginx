<script setup>

  import { Captions, CaptionsOff, Heart, MessageCircle, MonitorPlay, Settings, Tag } from 'lucide-vue-next';
  import { ref } from 'vue';
  const { post } = defineProps({
    post: Object
  })
  function titleCase(string){
    return string[0].toUpperCase() + string.slice(1).toLowerCase();
  }

  const showMore = ref(false)
  const hashtags = post.hashtags.length ? post?.hashtags?.slice(0,5)?.map((h) => `#${h}`)?.join(", ") : "-"
  const productType = titleCase(post?.product_type?.split("_")?.join(" "))


  const handleVisit = () => {
    window.open(post.url)
  }

  const handleShowMore = () => {
    showMore.value = !showMore.value
  }


</script>

<template>
    <div class="max-w-sm xl:w-2/5 w-96 xl:min-w-2/5 xl:max-w-full xl:h-96 xl:flex">
      <v-img :src="post.thumbnail" cover class="h-48 w-96 xl:h-auto xl:w-64 rounded-t xl:rounded-t-none xl:rounded-l  overflow-hidden" >
      </v-img>
      <div class="border-r border-b border-l -mt-2 xl:-mt-0 border-gray-300 xl:border-l-0 w-full xl:border-t xl:border-gray-300 shadow bg-white rounded-b xl:rounded-b-none xl:rounded-r p-4 flex flex-col justify-between leading-normal">
        <div class="mb-2 flex flex-col gap-3">
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
          <div class="text-gray-700 text-sm flex gap-2 w-full items-center">
            <MonitorPlay />
            <span>{{ productType }}</span>
          </div>

          <div class="text-gray-700 text-sm flex gap-2 w-full items-center">
            <Settings />
            <span>{{ post.eng_rate }}</span>
          </div>
          <div class="text-gray-700 flex gap-2 w-full">
            <Tag />
            <span class="text-balance"> {{ hashtags }} </span>
          </div>
        </div>

        <v-scrollbar v-if="showMore" class="text-gray-900 shadow-md  mt-2 xl:mt-auto mb-2 rounded-lg leading-none h-32">
          <div class="break-words overflow-y-auto h-full">
            {{ post.caption_text }}
          </div>
        </v-scrollbar>

          <!-- <img class="w-10 h-10 rounded-full mr-4" src="/img/jonathan.jpg" alt="Avatar of Jonathan Reinink"> -->
        <div class="text-sm flex items-center gap-1">
          <!-- <Button class=" w-32" @click="handleShowMore"> {{ showMore ? "Hide Caption" : "Show Caption" }}</Button> -->
          <div class="w-full">
            <p class="text-gray-600">{{ post?.upload_date?.$date.split("T")[0] }}</p>
          </div>
          <div class=" items-center gap-5 w-full flex justify-end">
            <v-btn icon @click="handleShowMore">
              <template v-slot:default>
                <CaptionsOff v-if="showMore" />
                <Captions v-else="showMore" />
              </template>
            </v-btn>
            <v-btn color='secondary' icon="mdi-chevron-right" @click="handleVisit" />
          </div>
        </div>

    </div>
  </div>
</template>
