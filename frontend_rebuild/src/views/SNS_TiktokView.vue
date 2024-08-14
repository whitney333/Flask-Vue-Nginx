<script setup>
    import PageHolder from '@/components/PageHolder.vue'
    import SNSCard from '@/components/SNS/SNS_card.vue'
    import SNSCardHolder from '@/components/SNS/SNS_card_holder.vue'
    import SNSHashtagAnalytics from '@/components/SNS/SNS_HashtagAnalytics.vue';
    import SNSTopicAnalytics from '@/components/SNS/SNS_TopicAnalytics.vue';

    const icon = "https://mishkan-ltd.s3.ap-northeast-2.amazonaws.com/web-img/tiktok-logo.svg"
    const tiktokFollowerValue = {
        chart: "tiktokFollower",
        title: "Tiktok Follower",
        type: 'Followers',
        tooltipText: "Number of followers on Tiktok",
        iconSrc: icon,
        fetchURL: "/api/tiktok/chart/follower",
        colors: ['#000000', '#000000'],
        fetchFollowerType: 'result',
        followerDataType: 'tiktok_follower',
        fetchDateType: 'datetime',
    }
    const tiktokTotalLikesValue = {
        chart: "tiktokTotalLikes",
        title: "Tiktok Total Likes",
        type: 'Likes',
        tooltipText: "Number of likes on Tiktok",
        iconSrc: icon,
        fetchURL: "/api/tiktok/chart",
        colors: ['#000000', '#000000'],
        fetchFollowerType: 'result',
        followerDataType: 'total_like',
        fetchDateType: 'datetime',
        secondChat: {
            chart: "tiktokAvgLikes",
            followerDataType: 'avg_like',
            fetchDateType: 'datetime',
            type: 'Likes per video'
        }

    }
    const tiktokTotalViewsValue = {
        chart: "tiktokTotalViews",
        title: "Tiktok Total Views",
        type: 'Views',
        tooltipText: "Number of views on Tiktok",
        iconSrc: icon,
        fetchURL: "/api/tiktok/chart",
        colors: ['#000000', '#000000'],
        fetchFollowerType: 'result',
        followerDataType: 'total_views',
        fetchDateType: 'datetime',
        secondChat: {
            chart: "tiktokAvgViews",
            followerDataType: 'avg_view',
            fetchDateType: 'datetime',
            type: 'Views per video'
        }
    }
    const tiktokTotalCommentsValue = {
        chart: "tiktokTotalComments",
        title: "Tiktok Total Comments",
        type: 'Comments',
        tooltipText: "Number of comments on TikTok",
        iconSrc: icon,
        fetchURL: "/api/tiktok/chart",
        colors: ['#000000', '#000000'],
        fetchFollowerType: 'result',
        followerDataType: 'total_comment',
        fetchDateType: 'datetime',
        secondChat: {
            chart: "tiktokAvgComments",
            followerDataType: 'avg_comment',
            fetchDateType: 'datetime',
            type: 'Comments per video'
        }
    }
    const tiktokTotalSharesValue = {
        chart: "tiktokTotalShares",
        title: "Tiktok Total Shares",
        type: 'Shares',
        tooltipText: "Number of shares on TikTok",
        iconSrc: icon,
        fetchURL: "/api/tiktok/chart",
        colors: ['#000000', '#000000'],
        fetchFollowerType: 'result',
        followerDataType: 'total_share',
        fetchDateType: 'datetime',
        secondChat: {
            chart: "tiktokAvgShares",
            followerDataType: 'avg_share',
            fetchDateType: 'datetime',
            type: 'Shares per video'
        }
    }

    const tiktokTotalSavesValue = {
        chart: "tiktokTotalSaves",
        title: "Tiktok Total Saves",
        type: 'Saves',
        tooltipText: "Number of saves on TikTok",
        iconSrc: icon,
        fetchURL: "/api/tiktok/chart",
        colors: ['#000000', '#000000'],
        fetchFollowerType: 'result',
        followerDataType: 'total_save',
        fetchDateType: 'datetime',
        secondChat: {
            chart: "tiktokAvgSaves",
            followerDataType: 'avg_save',
            fetchDateType: 'datetime',
            type: 'Saves per video'
        }
    }

    const tiktokEngagementRateValue = {
        chart: "tiktokEngagementRate",
        title: "Tiktok Engagement Rate",
        type: 'Engagement Rate',
        tooltipText: "Average engagment rate on Tiktok",
        iconSrc: icon,
        fetchURL: "/api/tiktok/chart",
        colors: ['#000000', '#000000'],
        fetchFollowerType: 'result',
        followerDataType: 'eng_rate',
        fetchDateType: 'datetime',
        percentageData: true,
    }

    const cardValueLists = [
        tiktokFollowerValue,
        tiktokTotalLikesValue,
        tiktokTotalViewsValue,
        tiktokTotalCommentsValue,
        tiktokTotalSharesValue,
        tiktokTotalSavesValue,
        tiktokEngagementRateValue,
    ]


    const hashtagAnalyticsValue = {
        iconSrc: icon,
        apiType: 'tiktok',
        usedCol: {
            tooltipText: "Daily trend of Tiktok Hashtags"
        },
        engagedCol: {
            tooltipText: "Daily trend of Tiktok Hashtags"
        }
        
    }

    const topAnalyticsValue = {
        iconSrc: icon,
        tooltipText: '',
        apiType: 'tiktok',
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
        <SNSAllPosts :value="allPostsValue"></SNSAllPosts>
</template>