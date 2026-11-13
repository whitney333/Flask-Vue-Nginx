import axiosAPI from 'axios'

/**
 * Axios client for unauthenticated public endpoints (e.g. artist share links).
 * Deliberately NOT the shared `@/axios` instance: that one attaches the admin's
 * Firebase token and signs the user out on 401, neither of which belongs here.
 */
const publicApi = axiosAPI.create({
  baseURL: import.meta.env.VITE_BASE_URL,
  headers: { 'Content-type': 'application/json' },
  timeout: 15000,
})

export default publicApi
