import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useArtistStore = defineStore('artist', () => {
  // const mid = ref(null)
  const artistId = ref(null)

  // function setMid(newMid) {
  //   mid.value = newMid
  // }

  function setArtist(newArtistId) {
    artistId.value = newArtistId
  }

  // function reset() {
  //   mid.value = null
  // }

  function reset() {
    artistId.value = null
  }

  // return { mid, setMid, reset }
  return {
    artistId,
    setArtist,
    reset
  }
}, {persist: true},
)
