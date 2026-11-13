/**
 * Loads Google Analytics 4 only when a measurement id is configured.
 * Named neutrally on purpose: ad blockers block files called "googleAnalytics.js", which
 * broke the whole app in dev (each module is fetched separately there).
 * Replaces the static snippet in index.html, which requested gtag.js with the literal
 * placeholder "%VITE_GA4_ID%" whenever the variable was missing (and made Vite warn).
 */

const GTAG_SRC = 'https://www.googletagmanager.com/gtag/js?id='

/**
 * @param {string | undefined} measurementId e.g. 'G-XXXXXXX'
 * @param {Window} [win] injectable for tests
 * @param {Document} [doc] injectable for tests
 * @returns {boolean} true when analytics was set up
 */
export function loadGoogleAnalytics(measurementId, win = window, doc = document) {
  if (!measurementId) return false

  win.dataLayer = win.dataLayer || []
  // gtag must push the `arguments` object itself, as Google's snippet does
  win.gtag = function gtag() {
    win.dataLayer.push(arguments) // eslint-disable-line prefer-rest-params
  }
  win.gtag('js', new Date())
  // page views are sent from the router (main.js) so share tokens never reach analytics
  win.gtag('config', measurementId, { send_page_view: false })

  const script = doc.createElement('script')
  script.async = true
  script.src = `${GTAG_SRC}${encodeURIComponent(measurementId)}`
  doc.head.appendChild(script)
  return true
}
