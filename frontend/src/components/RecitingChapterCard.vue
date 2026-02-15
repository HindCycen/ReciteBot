<template>
  <div
    class="bg-purple-50 border-l-4 border-l-purple-500 rounded-lg p-4 hover:shadow-md transition-all duration-200"
  >
    <div class="flex justify-between items-start mb-3">
      <div class="flex-1">
        <h3 class="text-lg font-semibold text-gray-800">
          {{ chapter.Title }}
        </h3>
        <p v-if="chapter.added_at" class="text-xs text-gray-500 mt-1">
          添加于: {{ formatDate(chapter.added_at) }}
        </p>
      </div>
      <button
        @click="removeFromReciteList"
        class="px-3 py-1 rounded text-sm font-medium transition-colors whitespace-nowrap ml-2 bg-red-500 hover:bg-red-600 text-white"
        title="移除"
        :disabled="isRemoving"
      >
        {{ isRemoving ? "移除中..." : "✕ 移除" }}
      </button>
    </div>
    <p class="text-gray-700 text-sm leading-relaxed whitespace-pre-wrap">
      {{ chapter.Content }}
    </p>
  </div>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  chapter: {
    type: Object,
    required: true,
  },
  bookName: {
    type: String,
    required: true,
  },
});

const emit = defineEmits(["remove-chapter"]);

const isRemoving = ref(false);

// 格式化日期
const formatDate = (dateString) => {
  try {
    const date = new Date(dateString);
    return date.toLocaleString("zh-CN");
  } catch {
    return dateString;
  }
};

// 从背诵列表移除
const removeFromReciteList = async () => {
  if (isRemoving.value) return;

  if (!window.confirm("确认要移除这个章节吗？")) {
    return;
  }

  isRemoving.value = true;
  try {
    emit("remove-chapter", props.bookName, props.chapter.Title);
  } finally {
    isRemoving.value = false;
  }
};
</script>
