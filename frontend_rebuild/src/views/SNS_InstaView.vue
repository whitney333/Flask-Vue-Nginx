<script setup>
    import PageHolder from '@/components/PageHolder.vue'
    import SNSCard from '@/components/SNS/SNS_card.vue'
    import SNSCardHolder from '@/components/SNS/SNS_card_holder.vue'
    import SNSHashtagAnalytics from '@/components/SNS/SNS_HashtagAnalytics.vue';
    import SNSTopicAnalytics from '@/components/SNS/SNS_TopicAnalytics.vue';

    const instaIcon = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/instagram-logo.svg"
    const instagramFollowerValue = {
        chart: "instagramFollower",
        title: "Instagram Follower",
        type: 'Followers',
        tooltipText: "Number of followers on Instagram",
        iconSrc: instaIcon,
        colors: ['#3F37C9', '#4895EF'],
        fetchURL: "/api/instagram/chart/follower",
        fetchFollowerType: 'result',
        followerDataType: 'follower_count',
        fetchDateType: 'datetime',
    }
    const instagramThreadsFollowerValue = {
        chart: "instagramThreadsFollower",
        title: "Instagram Threads Follower",
        type: 'Threads Followers',
        tooltipText: "Number of followers on Instagram Threads",
        iconSrc: instaIcon,
        colors: ['#3F37C9', '#4895EF'],
        fetchURL: "/api/instagram/threads/follower",
        fetchFollowerType: 'result',
        followerDataType: 'threads_followers',
        fetchDateType: 'datetime',
    }
    const instagramPostsValue = {
        chart: "instagramPosts",
        title: "Instagram Posts",
        type: 'Posts',
        tooltipText: "Number of posts on Instagram",
        iconSrc: instaIcon,
        colors: ['#3F37C9', '#4895EF'],
        fetchURL: "/api/instagram/chart/follower",
        fetchFollowerType: 'result',
        followerDataType: 'media_count',
        fetchDateType: 'datetime',
    }
    const instagramLikesValue = {
        chart: "instagramLikes",
        title: "Instagram Likes",
        type: 'Likes',
        tooltipText: "Number of Likes on Instagram",
        iconSrc: instaIcon,
        colors: ['#3F37C9', '#4895EF'],
        fetchURL: "/api/instagram/chart",
        fetchFollowerType: 'result',
        followerDataType: 'total_like',
        fetchDateType: 'datetime',
        secondChat: {
            chart: "instagramAvgLikes",
            followerDataType: 'avg_like',
            fetchDateType: 'datetime',
            type: 'Likes per post'
        }
    }
    const instagramCommentsValue = {
        chart: "instagramComments",
        title: "Instagram Comments",
        type: 'Comments',
        tooltipText: "Number of comments on Instagram",
        iconSrc: instaIcon,
        colors: ['#3F37C9', '#4895EF'],
        fetchURL: "/api/instagram/chart",
        fetchFollowerType: 'result',
        followerDataType: 'total_comment',
        fetchDateType: 'datetime',
        secondChat: {
            chart: "instagramAvgLikes",
            followerDataType: 'avg_comment',
            fetchDateType: 'datetime',
            type: 'Comments per post'
        }
    }

    const instagramEngagementRateValue = {
        chart: "instagramEngagementRate",
        title: "Instagram Engagement Rate",
        type: 'Engagement Rate',
        tooltipText: "Average engagment rate on Instagram",
        iconSrc: instaIcon,
        colors: ['#3F37C9', '#4895EF'],
        fetchURL: "/api/instagram/chart",
        fetchFollowerType: 'result',
        followerDataType: 'eng_rate',
        fetchDateType: 'datetime',
        percentageData: true,
    }

    const cardValueLists = [
        instagramFollowerValue,
        instagramThreadsFollowerValue,
        instagramPostsValue,
        instagramLikesValue,
        instagramCommentsValue,
        instagramEngagementRateValue,
    ]


    const hashtagAnalyticsValue = {
        iconSrc: instaIcon,
        apiType: 'instagram',
        usedCol: {
            tooltipText: "Daily trend of Instagram Hashtags"
        },
        engagedCol: {
            tooltipText: "Daily trend of Instagram Hashtags"
        }
        
    }

    const topAnalyticsValue = {
        iconSrc: instaIcon,
        tooltipText: '',
        apiType: 'instagram',
    }
    
    const allPostsValue = {

    }


</script>

<template>
    <v-container
    fluid
    :class="['bg-grey-lighten-4']">
        <div
        :class="['justify-center', 'd-flex', 'align-center']">
            <div
            :class="['justify-center','ga-4', 'd-flex', 'flex-wrap', 'align-center']">
                <div v-for="(card, index) in cardValueLists" :key="index">
                    <SNSCard :value="card"></SNSCard>
                </div>
            </div>
        </div>
    </v-container>
    <v-divider></v-divider>
        <SNSHashtagAnalytics :value="hashtagAnalyticsValue"></SNSHashtagAnalytics>
    <v-divider></v-divider>
        <SNSTopicAnalytics :value="topAnalyticsValue"></SNSTopicAnalytics>
    <v-divider></v-divider>
        <SNSAllPosts :value="allPostsValue"></SNSAllPosts>
</template>