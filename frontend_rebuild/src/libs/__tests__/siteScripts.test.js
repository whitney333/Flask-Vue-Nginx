import { test } from 'node:test'
import assert from 'node:assert/strict'
import { loadGoogleAnalytics } from '../siteScripts.js'

const fakeEnv = () => {
  const appended = []
  const doc = {
    createElement: (tag) => ({ tag }),
    head: { appendChild: (el) => appended.push(el) },
  }
  return { win: {}, doc, appended }
}

test('does nothing without a measurement id', () => {
  const { win, doc, appended } = fakeEnv()

  assert.equal(loadGoogleAnalytics('', win, doc), false)
  assert.equal(loadGoogleAnalytics(undefined, win, doc), false)
  assert.equal(appended.length, 0)
  assert.equal(win.gtag, undefined)
})

test('loads gtag.js once with the id and disables automatic page views', () => {
  const { win, doc, appended } = fakeEnv()

  assert.equal(loadGoogleAnalytics('G-TEST123', win, doc), true)

  assert.equal(appended.length, 1)
  assert.equal(appended[0].async, true)
  assert.equal(appended[0].src, 'https://www.googletagmanager.com/gtag/js?id=G-TEST123')
  assert.equal(typeof win.gtag, 'function')
  const config = win.dataLayer.map((args) => Array.from(args)).find((args) => args[0] === 'config')
  assert.deepEqual(config, ['config', 'G-TEST123', { send_page_view: false }])
})

test('encodes the id in the script url', () => {
  const { win, doc, appended } = fakeEnv()

  loadGoogleAnalytics('G-A&B', win, doc)

  assert.equal(appended[0].src, 'https://www.googletagmanager.com/gtag/js?id=G-A%26B')
})
