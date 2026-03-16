import { defineStore } from "pinia"
import { getAuth, onAuthStateChanged } from "firebase/auth"

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    idToken: null,
    ready: false
  }),

  actions: {
    init() {
      const auth = getAuth()

      onAuthStateChanged(auth, async (user) => {
        this.user = user
        this.idToken = user ? await user.getIdToken() : null
        this.ready = true
      })
    },

    async refreshToken() {
      if (this.user) {
        this.idToken = await this.user.getIdToken(true)
      }
    }
  }
})
