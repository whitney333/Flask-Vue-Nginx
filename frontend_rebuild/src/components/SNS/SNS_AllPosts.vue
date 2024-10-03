<script setup>
    import axios from '@/axios';
    import { computed, ref, watch } from 'vue';

    const postExamples = [
        {
            id: 0,
            followerCount: 150,
            
        }
    ]
    const posts = ref([])
    const postsCount = ref(0)
    const page = ref(1)
    const perPage = ref(9)
    const pages = ref([])
    const sort = ref('')
    const displayedPosts = computed(() => {
        return paginate(posts.value)
    })

    const getPosts = async () => {
        try {
            const res = await axios.get(`/api/instagram/post?page=${page.value}&limit=${perPage.value}&sort=${sort.value}`, {setTimeout: 10000})
            posts.value = res.data["result"]["posts"]
            postsCount.value = res.data["result"]["total_posts_count"]

        } catch (e) {
            console.error(e);
        }
    }

    const setPages =  () => {
        let numberOfPages = Math.ceil(posts.value.length / perPage.value);
        for (let index = 1; index <= numberOfPages; index++) {
        pages.value.push(index);
        }
    }

    const paginate =  (posts) => {
        let page = page.value;
        let perPage = perPage.value;
        let from = (page * perPage) - perPage;
        let to = (page * perPage);
        return  posts.slice(from, to);
    }

    watch(posts, () => setPages())
</script>
<template>
    <v-container
    fluid
    style="background-color: #f8f7f2;">
        <v-pagination :length="pages.length"></v-pagination>

    </v-container>
</template>