<script setup>
    const { region, changeState } = defineProps({
        region: Array,
        changeState: () => {}
    })
    const regions = {
      "Asia": ["Taiwan", "Hong Kong", "Japan", "South Korea", "Thailand", "Vietnam", "Philippines", "Indonesia"],
      "North America": ["United States", "Canada"],
      "South America": ["Brazil", "Mexico"],
      "Europe": ["United Kingdom", "Germany", "France", "Spain", "Italy"],
      "Oceania": ["Australia"],
    }
    const indexToCountry = ['Taiwan', 'Hong Kong', 'Japan', 'South Korea', 'Thailand', 'Vietnam', 'Philippines', 'Indonesia', 'United States', 'Canada', 'Brazil', 'Mexico', 'United Kingdom', 'Germany', 'France', 'Spain', 'Italy', 'Australia']

</script>

<template>
  <v-expansion-panel value="region" class="mb-5">
    <v-expansion-panel-title v-slot="{ expanded }">
      <v-row no-gutters class="items-center">
        <v-col class="d-flex justify-start" cols="4">
          <span class="text-2xl font-medium">
            {{ $t('Select Region') }}
          </span>
        </v-col>
        <v-col
          class="items-center"
          cols="8"
        >
          <v-fade-transition >
            <span
              v-if="!expanded"
              key="1"
              class="text-lg font-medium capitalize"
            >
              {{ region == '' ? '' :  region.map((r) => indexToCountry[r]).join(', ')}}
            </span>
          </v-fade-transition>
        </v-col>
      </v-row>
    </v-expansion-panel-title>
    <v-expansion-panel-text >
      <v-item-group multiple v-model="region">
        <v-container class="max-w-screen-md">
          <v-row>
            <v-row v-for="(reg, i) in Object.keys(regions)" :key="i" class="mb-5">
              <v-col cols="12">
                <span class="text-xl font-medium">
                  {{ reg }}
                </span>
              </v-col>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-5">
                  <v-col
                    v-for="(country, j) in regions[reg]"
                    :key="j"
                  >
                    <v-item v-slot="{ isSelected, toggle }">
                      <v-card
                        flat
                        class="d-flex align-center transition-all rounded-lg border-2 "
                        :class="isSelected ? ' border-black' : 'border-neutral-100'"
                        height="50"
                        width="150"
                        @click="toggle"
                      >
                        <v-scroll-y-transition>
                          <div
                            class="flex-grow-1 text-center text-lg font-medium"
                          >
                            {{ country }}
                          </div>
                        </v-scroll-y-transition>
                      </v-card>
                    </v-item>
                  </v-col>
                </div>

            </v-row>
          </v-row>
        </v-container>
      </v-item-group>
      <div class="my-5 flex justify-center items-center">
        <v-btn color='secondary'
        class="w-32 text-none text-white"
        @click="() => changeState('platform')">
          <span class="font-medium">
            {{ $t('Next') }}
          </span>
        </v-btn>
      </div>
    </v-expansion-panel-text>
  </v-expansion-panel>
</template>