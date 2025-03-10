<script setup>
    import axios from '@/axios';
    import { computed, onMounted, ref, watch } from 'vue';
    import SNS_TikTok_PostCard from '@/views/SNS/components/SNS_TikTok_PostCard.vue';
    import SNS_Insta_PostCard from '@/views/SNS/components/SNS_Insta_PostCard.vue';
    import SNS_Youtube_PostCard from '@/views/SNS/components/SNS_Youtube_PostCard.vue';

    const props = defineProps({
        posts: Object,
        platform: String,
    })
    const first = ref(1)
    const posts = ref([])

    const displayPosts = computed(() => {
            return posts.value.slice((first.value - 1) * 6, ((first.value - 1) * 6) + 6)
        }
    )    

    
    const fetchPosts = async () => {
        try {
            const res = await axios.get(`/${props.platform}/posts`)
            console.log(res.data.result);
            
            posts.value = res.data?.result
        } catch(e) {
            posts.value = postsExample
            // console.error(e);
            console.log(posts.value);
            
        }
    }
    onMounted(() => {
        fetchPosts()
    })


</script>
<template>
    <v-container
    fluid
    class=' bg-gray-100'>
        <!-- <div>Last update: {{ posts[0]?. }}</div> -->
        <div class="text-center mt-3 mb-5">
            <v-pagination
            v-model="first"
            :length="(posts[0]?.media_count - 1) / 6"
            rounded="circle"
            :total-visible="6"
            ></v-pagination>
        </div>

        <div class="flex justify-center items-center gap-10 flex-wrap md:gap-16 ">
            <template v-if="platform === 'tiktok'">
                <SNS_TikTok_PostCard :post="post" :key="`${post.url}_${first}`" v-for="(post) in displayPosts" />
            </template>
            <template v-if="platform === 'youtube'">
                <SNS_Youtube_PostCard :post="post" :key="`${post.url}_${first}`" v-for="(post) in displayPosts" />
            </template>
            <template v-if="platform === 'instagram'">
                <SNS_Insta_PostCard :post="post" :key="`${post.url}_${first}`" v-for="(post) in displayPosts" />
            </template>
        </div>
    </v-container>
</template>

<style>
    .custom-paginator {
    background-color: transparent !important;
    border: none !important;
    }

</style>