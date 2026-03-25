import axiosAPI from 'axios';
import { getAuth, signOut } from "firebase/auth";
import { useUserStore } from "@/stores/user";
import { useArtistStore } from "@/stores/artist";
import router from "@/router";

const axios = axiosAPI.create({
  baseURL: import.meta.env.VITE_BASE_URL ,
  headers: { "Content-type": "application/json" }
});

axios.interceptors.request.use(
  async (config) => {
    const auth = getAuth()
    const user = auth.currentUser
    if (user) {
      const token = await user.getIdToken()
      config.headers = config.headers || {}
      if (!config.headers.Authorization) {
        config.headers.Authorization = `Bearer ${token}`
      }
    }
    return config
  },
  (error) => Promise.reject(error)
)

axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response && error.response.status === 401) {
      const auth = getAuth()
      const userStore = useUserStore()
      const artistStore = useArtistStore()

      try {
        await signOut(auth)
        userStore.reset()
        artistStore.reset()
        router.push("/auth/login")
      } catch (e) {
        console.error("Sign-out error during 401 response:", e)
      }
    }
    return Promise.reject(error)
  }
)

export default axios;
