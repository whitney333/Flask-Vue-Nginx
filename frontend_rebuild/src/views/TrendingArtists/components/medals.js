/**
 * Gold / silver / bronze accents for the top 3, shared by the desktop podium
 * card and the mobile list rows so both render the same treatment.
 *
 * Class names are written out in full (not built dynamically) so Tailwind's
 * content scan can generate them.
 */
export const MEDALS = {
  1: { ring: 'ring-amber-400', badge: 'bg-amber-400 text-amber-950', glow: 'from-amber-50' },
  2: { ring: 'ring-slate-300', badge: 'bg-slate-300 text-slate-800', glow: 'from-slate-50' },
  3: { ring: 'ring-orange-300', badge: 'bg-orange-300 text-orange-950', glow: 'from-orange-50' },
}

export const MEDAL_PLACES = Object.keys(MEDALS).length

/** Medal accent for a 1-based rank, or null when the rank is outside the top 3. */
export const medalForRank = (rank) => MEDALS[rank] ?? null
