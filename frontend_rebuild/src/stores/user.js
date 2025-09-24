import { defineStore } from "pinia";

// store user token in pinia
export const useUserStore = defineStore("user", {
  state: () => ({
    firebase_id: null,
    email: null,
    name: null,
    photo: null,
    tenant: null,
    firebaseToken: null,
    followedArtists: []
  }),
  actions: {
    setUser(user) {
      this.firebase_id = user.firebase_id;
      this.email = user.email;
      this.name = user.name;
      this.photo = user.photo;
      this.tenant = user.tenant;
      this.followedArtists = user.followedArtists || [];
      this.firebaseToken = user.firebaseToken;
    },
    reset() {
      this.firebase_id = null
      this.email = null
      this.name = null
      this.photo = null
      this.tenant = null
      this.followedArtists = []
      this.firebaseToken = null
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
