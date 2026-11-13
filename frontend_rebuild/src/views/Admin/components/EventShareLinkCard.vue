<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import axios from '@/axios'

const props = defineProps({
  eventId: { type: String, required: true },
  hasShareLink: { type: Boolean, default: false },
  shareTokenCreatedAt: { type: String, default: null },
})

// notify: (message, color) toast; updated: ({ has_share_link, share_token_created_at }) for parent sync
const emit = defineEmits(['notify', 'updated'])

const hasLink = ref(props.hasShareLink)
const createdAt = ref(props.shareTokenCreatedAt)
// The link is stored server-side, so it can be fetched and copied again at any time.
const token = ref(null)
const loadingLink = ref(false)
const busy = ref(false)
const copied = ref(false)
// 'regenerate' | 'revoke' | null: destructive actions need a second click
const pendingAction = ref(null)

const COPIED_FEEDBACK_MS = 2000

watch(
  () => [props.hasShareLink, props.shareTokenCreatedAt],
  ([nextHasLink, nextCreatedAt]) => {
    hasLink.value = nextHasLink
    createdAt.value = nextCreatedAt
    if (!nextHasLink) token.value = null
    else if (!token.value) loadLink()
  }
)

const shareUrl = computed(() =>
  token.value ? `${window.location.origin}/share/events/${token.value}` : ''
)

const createdLabel = computed(() => {
  if (!createdAt.value) return ''
  const date = new Date(createdAt.value.endsWith('Z') ? createdAt.value : `${createdAt.value}Z`)
  return Number.isNaN(date.getTime()) ? '' : date.toLocaleString()
})

const errorMessage = (err, fallback) => err?.response?.data?.error || fallback

const loadLink = async () => {
  loadingLink.value = true
  try {
    const res = await axios.get(`/admin/v1/events/${props.eventId}/share`)
    token.value = res.data?.data?.share_token || null
    createdAt.value = res.data?.data?.share_token_created_at || null
    hasLink.value = Boolean(token.value)
  } catch (err) {
    emit('notify', errorMessage(err, 'Failed to load the share link.'), 'error')
  } finally {
    loadingLink.value = false
  }
}

onMounted(() => {
  if (hasLink.value) loadLink()
})

const createLink = async () => {
  const isRegenerate = pendingAction.value === 'regenerate'
  busy.value = true
  try {
    const res = await axios.post(`/admin/v1/events/${props.eventId}/share`)
    token.value = res.data?.data?.share_token || null
    createdAt.value = res.data?.data?.share_token_created_at || null
    hasLink.value = Boolean(token.value)
    emit('updated', { has_share_link: hasLink.value, share_token_created_at: createdAt.value })
    emit('notify', isRegenerate
      ? 'New link created. The old link no longer works.'
      : 'Share link created.', 'success')
  } catch (err) {
    emit('notify', errorMessage(err, 'Failed to create share link.'), 'error')
  } finally {
    busy.value = false
    pendingAction.value = null
  }
}

const revokeLink = async () => {
  busy.value = true
  try {
    await axios.delete(`/admin/v1/events/${props.eventId}/share`)
    hasLink.value = false
    createdAt.value = null
    token.value = null
    emit('updated', { has_share_link: false, share_token_created_at: null })
    emit('notify', 'Share link revoked. It no longer works.', 'success')
  } catch (err) {
    emit('notify', errorMessage(err, 'Failed to revoke share link.'), 'error')
  } finally {
    busy.value = false
    pendingAction.value = null
  }
}

const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(shareUrl.value)
    copied.value = true
    setTimeout(() => { copied.value = false }, COPIED_FEEDBACK_MS)
  } catch {
    emit('notify', 'Could not copy automatically. Select the link and copy it manually.', 'error')
  }
}

const confirmPending = () => (pendingAction.value === 'revoke' ? revokeLink() : createLink())
</script>

<template>
  <section class="bg-white rounded-xl shadow p-6 border border-gray-200" aria-labelledby="share-link-heading">
    <div class="flex flex-col gap-1 sm:flex-row sm:items-start sm:justify-between">
      <div>
        <h3 id="share-link-heading" class="text-lg font-semibold text-gray-800">Artist Share Link</h3>
        <p class="text-sm text-gray-500">
          A private, read-only report page. Anyone with the link can view it without logging in.
        </p>
      </div>
      <span
          class="mt-2 inline-flex w-fit items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-semibold sm:mt-0"
          :class="hasLink ? 'bg-emerald-50 text-emerald-700' : 'bg-gray-100 text-gray-500'"
      >
        <span class="h-1.5 w-1.5 rounded-full" :class="hasLink ? 'bg-emerald-500' : 'bg-gray-400'"></span>
        {{ hasLink ? 'Active' : 'No link' }}
      </span>
    </div>

    <!-- No link yet -->
    <div v-if="!hasLink" class="mt-4">
      <button
          type="button"
          :disabled="busy"
          class="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-indigo-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600 disabled:opacity-50"
          @click="createLink"
      >
        {{ busy ? 'Creating…' : 'Create share link' }}
      </button>
    </div>

    <div v-else class="mt-4 space-y-3">
      <p v-if="loadingLink" class="text-sm text-gray-500" role="status">Loading link…</p>
      <template v-else-if="token">
        <div class="flex flex-col gap-2 sm:flex-row">
          <label for="share-link-url" class="sr-only">Share link</label>
          <input
              id="share-link-url"
              :value="shareUrl"
              readonly
              class="min-w-0 flex-1 rounded-lg border border-gray-300 bg-gray-50 px-3 py-2 font-mono text-xs text-gray-700 focus:border-indigo-500 focus:outline-none focus:ring-1 focus:ring-indigo-500"
              @focus="$event.target.select()"
          />
          <button
              type="button"
              class="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white transition hover:bg-indigo-700 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
              @click="copyLink"
          >
            {{ copied ? 'Copied ✓' : 'Copy link' }}
          </button>
        </div>
        <p class="text-xs text-gray-500">
          This link stays the same until you regenerate or revoke it.<template v-if="createdLabel"> Created {{ createdLabel }}.</template>
        </p>
      </template>

      <!-- Two-step confirm for destructive actions -->
      <div
          v-if="pendingAction"
          class="flex flex-col gap-3 rounded-lg border border-amber-200 bg-amber-50 p-3 text-sm text-amber-900 sm:flex-row sm:items-center sm:justify-between"
          role="alert"
      >
        <span>
          {{ pendingAction === 'revoke'
            ? 'Revoke this link? Anyone using it will lose access.'
            : 'Create a new link? The current link will stop working immediately.' }}
        </span>
        <div class="flex gap-2">
          <button
              type="button"
              class="rounded-lg border border-amber-300 bg-white px-3 py-1.5 font-medium hover:bg-amber-100"
              :disabled="busy"
              @click="pendingAction = null"
          >Cancel</button>
          <button
              type="button"
              class="rounded-lg px-3 py-1.5 font-semibold text-white disabled:opacity-50"
              :class="pendingAction === 'revoke' ? 'bg-red-600 hover:bg-red-700' : 'bg-amber-600 hover:bg-amber-700'"
              :disabled="busy"
              @click="confirmPending"
          >{{ busy ? 'Working…' : (pendingAction === 'revoke' ? 'Revoke' : 'Create new link') }}</button>
        </div>
      </div>

      <div v-else class="flex flex-wrap gap-2">
        <a
            v-if="token"
            :href="shareUrl"
            target="_blank"
            rel="noopener noreferrer"
            class="rounded-lg border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-700 transition hover:bg-gray-100"
        >Preview</a>
        <button
            type="button"
            class="rounded-lg border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-700 transition hover:bg-gray-100"
            @click="pendingAction = 'regenerate'"
        >Regenerate</button>
        <button
            type="button"
            class="rounded-lg border border-red-200 px-3 py-1.5 text-sm font-medium text-red-600 transition hover:bg-red-50"
            @click="pendingAction = 'revoke'"
        >Revoke</button>
      </div>
    </div>
  </section>
</template>
