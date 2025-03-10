<script setup>
    import axios from '@/axios';
    import { computed, onMounted, ref, watch } from 'vue';
    import Paginator from 'primevue/paginator';
    import SNS_TikTok_PostCard from '@/views/SNS/components/SNS_TikTok_PostCard.vue';
    import SNS_Insta_PostCard from '@/views/SNS/components/SNS_Insta_PostCard.vue';
    import SNS_Youtube_PostCard from '@/views/SNS/components/SNS_Youtube_PostCard.vue';

    const props = defineProps({
        posts: Object,
        platform: String,
    })
    const first = ref(0)
    const posts = ref([])

    const displayPosts = computed(() => {
            return posts.value.slice(first.value, first.value + 6)
        }
    )    

    
    const fetchPosts = async () => {
        try {
            const res = await axios.get(`/${props.platform}/posts`)
            console.log(res.data);
            
            posts.value = res.data.result
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
        <Paginator class="mb-5 bg-transparent" v-model:first="first" :rows="6" :totalRecords="posts[0]?.media_count">
        </Paginator>
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