import { defineStore } from "pinia";
import { getAuth } from "firebase/auth"

// store user token in pinia
export const useUserStore = defineStore("user", {
  state: () => ({
    firebase_id: null,
    email: null,
    name: null,
    photo: null,
    tenant: null,
    firebaseToken: null,
    followedArtists: [],
    admin: null,
    created_at: null,
    last_login_at: null,
    isPremium: null,
    plan: null,
    expiredAt: null
  }),
  actions: {
    // get user state in backend
    async fetchMe() {
      const userStore = useUserStore()
      const auth = getAuth()
      const user = auth.currentUser

      if (!user) {
        console.log("[userStore] fetchMe skipped: no user logged in")
        return
      }
      // refresh token
      const idToken = await user.getIdToken(true)

      try {
        const res = await fetch("/api/user/me", {
          headers: {
            Authorization: `Bearer ${idToken}`
          }
        })

        if (!res.ok) {
          throw new Error("fetchMe failed")
        }

        const user = await res.json()
        this.setUser(user)
      } catch (err) {
        console.error("[userStore] fetchMe error:", err)
      }
    },
    // update user state
    setUser(user) {
      this.firebase_id = user.firebase_id;
      this.email = user.email;
      this.name = user.name;
      this.photo = user.photo;
      this.tenant = user.tenant;
      this.followedArtists = user.followedArtists || [];
      this.firebaseToken = user.firebaseToken;
      this.admin = user.admin;
      this.created_at = user.created_at;
      this.last_login_at = user.last_login_at;
      this.isPremium = !!user.is_premium;
      this.plan = user.plan;
      this.expiredAt = user.expired_at;
    },
    reset() {
      this.firebase_id = null
      this.email = null
      this.name = null
      this.photo = null
      this.tenant = null
      this.followedArtists = []
      this.firebaseToken = null
      this.admin = null
      this.created_at = null
      this.last_login_at = null
      this.isPremium = false
      this.plan = null
      this.expiredAt = null
    },
    setFollowedArtists(artists) {
      // console.log("Setting followedArtists in store:", artists);
      this.followedArtists = artists || [];
    },
    removeFollowedArtist(artistId) {
      this.followedArtists = this.followedArtists.filter(
          a => a.artist_id !== artistId
      );
    },
  },
  persist: true
});
