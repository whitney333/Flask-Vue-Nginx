<script setup>
  import { Captions, CaptionsOff, Heart, MessageCircle, MonitorPlay, Settings } from 'lucide-vue-next';
  import { ref, computed } from 'vue';

  const props = defineProps({
    post: Object
  });

  const formatNumFunc = (value, isPercent = false) => {
    const num = Number(value || 0)

    const units = [
      {value: 1e9, suffix: 'B'},
      {value: 1e6, suffix: 'M'},
      {value: 1e3, suffix: 'K'},
    ]

    const unit = units.find(u => num >= u.value)

    const format = (val, suffix = '') => {
      const formatted =
          val % 1 === 0
              ? val.toString()
              : val.toFixed(1).replace(/\.0$/, '')

      return `${formatted}${suffix}${isPercent ? '%' : ''}`
    }

    if (unit) {
      return format(num / unit.value, unit.suffix)
    }

    return `${num.toLocaleString()}${isPercent ? '%' : ''}`
  }

  function titleCase(string){
    if (!string) return '';
    return string[0].toUpperCase() + string.slice(1).toLowerCase();
  }

  const showMore = ref(false);
  const showAllHashtags = ref(false);
  const productType = computed(() => titleCase(props.post?.type));

  const handleVisit = () => {
    if (props.post?.post_url) {
      window.open(props.post.post_url);
    }
  };

  const handleShowMore = () => {
    showMore.value = !showMore.value;
  };

  const visibleHashtags = computed(() => {
    const tags = props.post?.hashtags || [];
    // display 3 hashtags by default
    return showAllHashtags.value ? tags : tags.slice(0, 3);
  });

  const hiddenHashtagCount = computed(() => {
    const tags = props.post?.hashtags || [];
    return Math.max(0, tags.length - 3);
  });

  const toggleHashtags = () => {
    showAllHashtags.value = !showAllHashtags.value;
  };
</script>

<template>
  <div class="w-full max-w-sm sm:max-w-md xl:w-2/5 xl:max-w-full
            flex flex-col xl:flex-row
            h-auto xl:h-96
            overflow-hidden bg-white shadow rounded">

    <!-- image -->
    <v-img
      v-if="post?.thumbnail"
      :src="post.thumbnail"
      cover
      class="w-full h-48 sm:h-56 xl:w-64 xl:h-full flex-shrink-0"
    />

    <!-- content -->
    <div class="flex flex-col justify-between w-full p-4 overflow-visible min-w-0">

      <div class="flex flex-col gap-3 overflow-visible">

        <!-- stats -->
        <div class="flex gap-4 text-gray-700 text-sm">

          <!-- Likes -->
          <div class="relative group flex items-center gap-1 cursor-default">
            <Heart class="w-4 h-4"/>
            <span>{{ formatNumFunc(post?.like_count) }}</span>
          </div>

          <!-- Comments -->
          <div class="relative group flex items-center gap-1 cursor-default">
            <MessageCircle class="w-4 h-4"/>
            <span>{{ formatNumFunc(post?.comment_count) }}</span>
          </div>
        </div>

        <!-- Type -->
        <div class="relative group flex items-center gap-2 text-gray-700 text-sm cursor-default">
          <MonitorPlay class="w-4 h-4"/>
          <span>{{ productType }}</span>
        </div>

        <!-- Engagement Rate -->
        <div class="relative group flex items-center gap-2 text-gray-700 text-sm cursor-default">
          <Settings class="w-4 h-4"/>
          <span>{{ formatNumFunc(post?.eng_rate) }}</span>

        </div>

        <!-- Hashtags (clean small chips) -->
        <div class="flex flex-wrap gap-1 sm:gap-2 mt-2">
          <span
              v-for="(tag, i) in visibleHashtags"
              :key="i"
              class="
              px-1.5 py-0.5 text-[10px]
              sm:px-2 sm:py-1 sm:text-xs
              md:px-2.5 md:py-1 md:text-sm
              leading-none rounded-full
              bg-blue-50 text-blue-600
              hover:bg-blue-100 transition
              cursor-default border border-blue-100
            "
          >
            {{ tag.startsWith('#') ? tag : `${tag}` }}
          </span>

          <span
              v-if="hiddenHashtagCount > 0"
              @click="toggleHashtags"
              class="
              px-1.5 py-0.5 text-[10px]
              sm:px-2 sm:py-1 sm:text-xs
              md:px-2.5 md:py-1 md:text-sm
              leading-none rounded-full
              bg-blue-100 text-blue-700
              hover:bg-blue-200 transition
              cursor-default font-medium
            "
          >
            {{ showAllHashtags ? 'less' : `+${hiddenHashtagCount}` }}
          </span>
        </div>

        <!-- date -->
        <p class="text-xs text-gray-400 whitespace-nowrap">
          {{ post?.taken_at?.slice(0, 10) }}
        </p>

        <!-- caption -->
        <div
          v-if="showMore"
          class="h-24 overflow-y-auto text-gray-800 text-sm leading-snug rounded bg-gray-50 p-2"
        >
          {{ post?.caption_text }}
        </div>

      </div>

      <!-- bottom actions -->
      <div class="text-sm flex items-center justify-between mt-2">
        <div class="flex items-center gap-2">

          <v-btn icon @click="handleShowMore">
            <CaptionsOff v-if="showMore"/>
            <Captions v-else/>
          </v-btn>

          <v-btn
            color="secondary"
            icon="mdi-chevron-right"
            @click="handleVisit"
          />

        </div>
      </div>

    </div>
  </div>
</template>
