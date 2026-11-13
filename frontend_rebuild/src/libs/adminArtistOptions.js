import axios from '@/axios'
import { createArtistOptionsLoader } from './artistOptions.js'

// One shared loader: the list is fetched at most once per visit across admin pages.
export const loadAdminArtistOptions = createArtistOptionsLoader(async () => {
  const res = await axios.get('/admin/v1/artists/list')
  return res.data?.data
})
