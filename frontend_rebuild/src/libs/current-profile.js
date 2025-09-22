import axios from "@/axios"
import { getAuth } from "firebase/auth"
import { useRouter } from "vue-router"

export const currentProfile = async () => {
  const { currentUser } = getAuth()
  const router = useRouter()

  if (!currentUser) {
    return null
  }

  try {
    const res = await axios.get(`/v1/auth/user/${currentUser.uid}`)
    const profile = res.data.result
    
    return profile

  } catch(error) {
    console.error("Error fetching profile:", error)
    // If there's an error, redirect to login
    await router.push('/auth/login')
    return null
  }
}
