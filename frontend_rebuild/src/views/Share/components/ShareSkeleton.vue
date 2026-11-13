<template>
  <div class="mx-auto max-w-5xl animate-pulse px-4 pb-16 pt-6 sm:px-6 sm:pt-10" role="status" aria-live="polite">
    <span class="sr-only">Loading report…</span>
    <div class="flex items-center gap-4">
      <div class="h-12 w-12 rounded-2xl bg-indigo-100/60 sm:h-14 sm:w-14"></div>
      <div class="space-y-2">
        <div class="h-3 w-20 rounded-full bg-indigo-100/60"></div>
        <div class="h-6 w-64 max-w-[60vw] rounded-full bg-indigo-100/60"></div>
        <div class="h-3 w-48 rounded-full bg-indigo-100/60"></div>
      </div>
    </div>
    <div class="mt-6 grid grid-cols-1 gap-3 sm:gap-4 lg:grid-cols-6">
      <div class="h-56 rounded-3xl bg-indigo-200/50 lg:col-span-4"></div>
      <div class="h-56 rounded-3xl bg-indigo-100/60 lg:col-span-2"></div>
      <div class="h-64 rounded-3xl bg-indigo-100/60 lg:col-span-3"></div>
      <div class="h-64 rounded-3xl bg-indigo-100/60 lg:col-span-3"></div>
      <div class="h-40 rounded-3xl bg-indigo-100/60 lg:col-span-2"></div>
      <div class="h-40 rounded-3xl bg-indigo-100/60 lg:col-span-2"></div>
      <div class="h-40 rounded-3xl bg-indigo-100/60 lg:col-span-2"></div>
    </div>
  </div>
</template>
