import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useArtistStore = defineStore('artist', () => {
  const mid = ref(null)

  function setMid(newMid) {
    mid.value = newMid
  }

  function reset() {
    mid.value = null
  }

  return { mid, setMid, reset }
})
