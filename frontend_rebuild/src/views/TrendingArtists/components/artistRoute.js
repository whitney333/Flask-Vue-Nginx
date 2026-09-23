/**
 * Build the router location for an artist's detail page from a normalized
 * trending-list item. Shared by the list row (TA_card) and the podium card
 * so both navigate with identical params/query.
 *
 * Returns null when the item has no artist id.
 */
export const buildArtistRoute = (artist, year, week) => {
  const artistId = artist?.artistId ?? artist?.artist_id ?? ''
  if (!artistId) {
    return null
  }

  const artistName = artist?.artistName ?? artist?.english_name ?? artist?.korean_name ?? '-'

  return {
    name: 'Artist',
    params: {
      artistId,
      artistName,
    },
    query: {
      rank: artist?.rank,
      image: artist?.artistImg ?? artist?.image ?? '',
      koreanName: artist?.artistKoreanName ?? artist?.korean_name ?? '',
      type: artist?.type || '-',
      popularityScore: artist?.popularity ?? artist?.popularity_score ?? 0,
      musicScore: artist?.music_score ?? 0,
      snsScore: artist?.sns_score ?? 0,
      dramaScore: artist?.drama_score ?? 0,
      year,
      week,
    },
  }
}
