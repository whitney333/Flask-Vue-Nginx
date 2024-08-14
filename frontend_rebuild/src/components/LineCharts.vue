
<script setup>
import axios from '@/axios';
import { ref } from 'vue';

const props = defineProps({
    chartOptions: Object,
    series: Object,
    width: String,
    height: String,
    refItem: Object
})


</script>

<template>
    <div id="chart">
        <apexchart :ref="props.refItem" :width="props.width" :height="props.height" type="line" :options="props.chartOptions" :series="props.series"></apexchart>
    </div>
</template>