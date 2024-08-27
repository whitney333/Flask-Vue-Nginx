<script setup>
    import axios from '@/axios';

    const postExamples = [
        {
            id: 0,
            followerCount: 150,
            
        }
    ]

    // const  getPosts = async () => {
    //     const {data} = await axios.get('/api/instagram/post?' + 'page=' + this.page + '&limit=' + this.perPage + '&sort=' + this.sort)
    //     const page = data["result"]["page"]
    //     const sort = data["result"]["sort"]
    //     const total_posts_count = data["result"]["total_posts_count"]
    //     const InstaPost = data["result"]["posts"]
    //   // console.log(this.sort)
    //   //calculate subtotals
    //     const SubTotals = {};
    //     const columns = ['comment_count', 'like_count'];

    //     this.InstaPost.forEach(b => {
    //         let rowTotal = 0;
    //         columns.forEach(i => {
    //             if (b[i] === undefined) {
    //             return;
    //         }

    //         SubTotals[i] = SubTotals[i] || 0;
    //         SubTotals[i] += b[i];
    //         rowTotal += b[i];
    //         })
    //         b.RowTotal = rowTotal;
    //     });


    //     // Calculate RowTotal for ColumnsTotals
    //     columns.forEach(i => {
    //         SubTotals.RowTotal = SubTotals.RowTotal || 0;
    //         SubTotals.RowTotal += SubTotals[i];
    //     })
    //     this.subTotalNum = SubTotals.RowTotal
    //     // console.log(this.subTotalNum)
    // }

    
</script>
<template>
    <v-container
    fluid
    style="background-color: #f8f7f2;">
        <v-pagination :length="4"></v-pagination>

    </v-container>
</template>