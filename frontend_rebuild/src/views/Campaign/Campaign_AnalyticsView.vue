<script setup>
</script>

<template>
    <v-container
        fluid
        :class="['fill-height', 'align-start', 'bg-grey-lighten-4']">
            <v-card
            flat
            class="bg-[#F5F5F5]">
                <template v-slot:title>
                    <span class="text-h4">{{ $t('Report') }}</span>
                </template>
            </v-card>
    </v-container>
</template>
