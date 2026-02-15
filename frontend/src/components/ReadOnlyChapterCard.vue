<template>
  <div
    class="bg-gray-50 border-l-4 border-blue-500 rounded-lg p-4 hover:shadow-md transition-all duration-200"
  >
    <h3 class="text-lg font-semibold text-gray-800 mb-2">
      {{ chapter.Title }}
    </h3>
    <p class="text-gray-700 text-sm leading-relaxed whitespace-pre-wrap">
      {{ chapter.Content }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  chapter: {
    type: Object,
    required: true,
  },
});
</script>
