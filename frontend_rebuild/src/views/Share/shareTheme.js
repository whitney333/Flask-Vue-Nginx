/**
 * Colour and surface tokens for the public share page.
 * Full Tailwind class strings (no string building) so Tailwind's scanner keeps them.
 */

// Frosted card over the tinted page background
export const CARD =
  'share-rise rounded-3xl bg-white/70 p-5 shadow-[0_1px_2px_rgba(30,27,75,0.04),0_8px_24px_-12px_rgba(30,27,75,0.12)] ring-1 ring-indigo-950/5 backdrop-blur-xl transition duration-300 hover:-translate-y-0.5 hover:shadow-[0_2px_4px_rgba(30,27,75,0.05),0_16px_32px_-12px_rgba(30,27,75,0.18)] motion-reduce:transition-none motion-reduce:hover:translate-y-0 sm:p-6 print:break-inside-avoid print:bg-white print:shadow-none print:backdrop-blur-none'

// Small uppercase card titles
export const EYEBROW = 'text-[11px] font-semibold uppercase tracking-[0.14em] text-slate-500'

export const SERIES = Object.freeze({
  ticket: {
    fill: 'bg-gradient-to-r from-indigo-500 to-violet-500',
    track: 'bg-indigo-100/70',
    dot: 'bg-indigo-500',
    badge: 'bg-indigo-50 text-indigo-700 ring-1 ring-indigo-600/15',
  },
  benefit: {
    fill: 'bg-gradient-to-r from-amber-400 to-orange-500',
    track: 'bg-amber-100/80',
    dot: 'bg-orange-500',
    badge: 'bg-amber-50 text-orange-700 ring-1 ring-orange-600/15',
  },
})

// Distinct, non-stereotyped hues, largest group first
export const GENDER_FILLS = Object.freeze(['bg-violet-500', 'bg-teal-400', 'bg-slate-400', 'bg-slate-300'])

// Light-to-deep scale for age buckets (index from shadeIndex)
export const AGE_SHADES = Object.freeze([
  'bg-indigo-200',
  'bg-indigo-300',
  'bg-indigo-400',
  'bg-indigo-500',
  'bg-gradient-to-r from-indigo-500 to-violet-600',
])
