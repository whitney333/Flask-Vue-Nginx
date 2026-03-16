// stores/artist.js
import {defineStore} from 'pinia'
import {ref} from 'vue'
import axios from '@/axios'
import {getAuth} from 'firebase/auth'

export const useArtistStore = defineStore('artist', () => {
    const artistId = ref(null)
    const artist = ref({
        id: null,
        threads: null,
        instagram_id: null,
        youtube_id: null,
        tiktok_id: null,
        bilibili_id: null,
        spotify_id: null,
        melon_id: null,
        genie_id: null,
        apple_id: null,
    })

    // fetch artist info by ID
    async function fetchArtistInfo(id) {
        if (!id) return null
        try {
            const resp = await axios.get(`/artist/info?artist_id=${id}`)
            const data = resp.data?.data?.[0] || null
            if (!data) return null

            return {
                id: data._id || null,
                threads: data.threads || null,
                instagram_id: data.instagram_id || null,
                youtube_id: data.youtube_id || null,
                tiktok_id: data.tiktok_id || null,
                bilibili_id: data.bilibili_id || null,
                spotify_id: data.spotify_id || null,
                melon_id: data.melon_id || null,
                genie_id: data.genie_id || null,
                apple_id: data.apple_id || null,
            }
        } catch (err) {
            console.error('fetchArtistInfo error:', err)
            return null
        }
    }

    async function setArtistId(id) {
        artistId.value = id

        if (!id) {
            artist.value = {
                id: null,
                threads: null,
                instagram_id: null,
                youtube_id: null,
                tiktok_id: null,
                bilibili_id: null,
                spotify_id: null,
                melon_id: null,
                genie_id: null,
                apple_id: null,
            }
            return
        }

        const info = await fetchArtistInfo(id)
        artist.value = info || {
            id: null,
            threads: null,
            instagram_id: null,
            youtube_id: null,
            tiktok_id: null,
            bilibili_id: null,
            spotify_id: null,
            melon_id: null,
            genie_id: null,
            apple_id: null,
        }
    }

    function setArtist(newArtistId) {
        artist.value = newArtistId
    }

    function reset() {
        artistId.value = null
        artist.value = {
            id: null,
            threads: null,
            instagram_id: null,
            youtube_id: null,
            tiktok_id: null,
            bilibili_id: null,
            spotify_id: null,
            melon_id: null,
            genie_id: null,
            apple_id: null,
        }
    }

    return {
        artistId,
        artist,
        setArtist,
        setArtistId,
        fetchArtistInfo,
        reset
    }
}, {persist: true},)
