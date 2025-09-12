import axios from "@/axios"
import { getAuth } from "firebase/auth"

export const currentProfile = async () => {
  const auth = getAuth()
  const user = auth.currentUser

  // if not login
  if (!user) return null

  try {
    // check if database has this user
    const res = await axios.post("/user/v1/auth/check", {
      firebase_id: user.uid
    })

    return res.data.exists
  } catch(error) {
    console.error("Error fetching profile:", error)
    return false
  }
}
