/**
 * The admin artist dropdown list (~1.6k artists) is only needed while a form is open,
 * so it is fetched on first use and shared for the rest of the visit.
 */

/**
 * @param {() => Promise<unknown>} fetchList resolves to the artist array
 * @returns {() => Promise<Array<object>>} call it whenever the list is needed
 */
export function createArtistOptionsLoader(fetchList) {
  let pending = null
  return function loadArtistOptions() {
    if (!pending) {
      pending = Promise.resolve()
        .then(fetchList)
        .then((list) => (Array.isArray(list) ? list : []))
        .catch((error) => {
          pending = null // let the next form open retry
          throw error
        })
    }
    return pending
  }
}

/**
 * Artists to show for the selected ids: the full list when loaded (covers newly picked
 * artists), otherwise the event's own artists from the event response.
 * @param {Array<string|number>|undefined} selectedIds
 * @param {Array<{id: string}>} options full dropdown list, possibly empty
 * @param {Array<{id: string}>|undefined} eventArtists artists from the event payload
 */
export function resolveSelectedArtists(selectedIds, options, eventArtists) {
  const byId = new Map([
    ...(eventArtists || []).map((artist) => [String(artist.id), artist]),
    ...(options || []).map((artist) => [String(artist.id), artist]),
  ])
  return (selectedIds || []).map(String).map((id) => byId.get(id)).filter(Boolean)
}
