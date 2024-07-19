
<script setup>
import axios from '@/axios';
import { ref } from 'vue';

const props = defineProps({
    chartOptions: Object,
    series: Object,
})


</script>

<template>
    <div id="chart">
        <apexchart width="100%" height="100%" type="area" :options="props.chartOptions" :series="props.series"></apexchart>
    </div>
</template>
