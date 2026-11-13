import { test } from 'node:test'
import assert from 'node:assert/strict'
import { createArtistOptionsLoader, resolveSelectedArtists } from '../artistOptions.js'

const LIST = [
  { id: 'a1', artist_en_name: 'NOVA', artist_kr_name: '노바', image: 'y.jpg' },
  { id: 'a2', artist_en_name: 'LUMEN', artist_kr_name: '루멘', image: 's.jpg' },
]

test('loads the artist list once and reuses it for the rest of the visit', async () => {
  let calls = 0
  const load = createArtistOptionsLoader(async () => { calls += 1; return LIST })

  const [first, second] = await Promise.all([load(), load()])
  const third = await load()

  assert.equal(calls, 1)
  assert.deepEqual(first, LIST)
  assert.equal(second, first)
  assert.equal(third, first)
})

test('a failed load is not cached, so opening the form again retries', async () => {
  let calls = 0
  const load = createArtistOptionsLoader(async () => {
    calls += 1
    if (calls === 1) throw new Error('network down')
    return LIST
  })

  await assert.rejects(load(), /network down/)
  assert.deepEqual(await load(), LIST)
  assert.equal(calls, 2)
})

test('a non-array response becomes an empty list', async () => {
  const load = createArtistOptionsLoader(async () => ({ unexpected: true }))
  assert.deepEqual(await load(), [])
})

test('selected artists come from the event itself before the full list is loaded', () => {
  const eventArtists = [{ id: 'a1', artist_en_name: 'NOVA', artist_kr_name: '노바', image: 'y.jpg' }]

  assert.deepEqual(resolveSelectedArtists(['a1'], [], eventArtists), eventArtists)
})

test('newly picked artists are found in the full list once it is loaded', () => {
  const eventArtists = [{ id: 'a1', artist_en_name: 'NOVA (old)' }]

  const result = resolveSelectedArtists(['a1', 'a2'], LIST, eventArtists)

  assert.deepEqual(result.map((a) => a.artist_en_name), ['NOVA', 'LUMEN'])
})

test('ids are compared as strings and unknown ids are skipped', () => {
  assert.deepEqual(resolveSelectedArtists([2, 'zz'], [{ id: '2', artist_en_name: 'X' }], []), [
    { id: '2', artist_en_name: 'X' },
  ])
  assert.deepEqual(resolveSelectedArtists(undefined, LIST, undefined), [])
})
