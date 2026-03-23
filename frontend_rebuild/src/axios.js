import axiosAPI from 'axios';
import { getAuth } from "firebase/auth";

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

export default axios;
