
<script setup>
import axios from '@/axios';
import { ref } from 'vue';

const props = defineProps({
    chartOptions: Object,
    series: Object,
    width: String,
    height: String
})


</script>

<template>
    <div id="chart">
        <apexchart :width="props.width" :height="props.height" type="area" :options="props.chartOptions" :series="props.series"></apexchart>
    </div>
</template>
