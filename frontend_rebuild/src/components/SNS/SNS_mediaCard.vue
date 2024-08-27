<script setup>
    const props = defineProps({
        value: Object
    })

</script>

<template>
    <v-card>
        <v-row>
            <v-col :class="['shrink']">
                <v-img
                :max-width="80"
                :src="props.value.imgSrc">
                </v-img>
            </v-col>
            <v-col>
                <template v-slot:title>
                    {{ props.value.title }}
                </template>
            </v-col>
        </v-row>
    </v-card>
</template>