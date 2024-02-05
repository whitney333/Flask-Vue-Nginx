<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-img
          :src="require('../assets/logo.svg')"
          class="my-3"
          contain
          height="200"
        />
      </v-col>

      <v-col class="mb-4">
        <h1 class="display-2 font-weight-bold mb-3">
          Welcome to Vuetify
        </h1>
        <h3>Random Number: {{rand}}</h3>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  export default {
    name: 'HelloWorld',

    data: () => ({
      rand: 0,
    }),
    methods: {
      async get_random() {
        await this.axios({method: "GET", "url": "/api/rand"})
            .then(result => {
              this.rand = result.data["randomNum"];
              // console.log(this.rand)
            }, error => {
              console.error(error);
            });
      }
    },
    created() {
      this.get_random();
    }
  }
</script>
