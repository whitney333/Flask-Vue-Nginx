<template>
    <v-container
        fluid
        :class="['fill-height', 'align-start', 'bg-grey-lighten-4']">
            <v-card
            flat
            class="bg-grey-lighten-4">
                <template v-slot:title>
                    <span class="text-h4">{{ $t('Report') }}</span>
                </template>
            </v-card>
    </v-container>
</template>
