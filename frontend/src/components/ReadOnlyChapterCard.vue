<template>
  <div
    :class="[
      'bg-gray-50 border-l-4 rounded-lg p-4 hover:shadow-md transition-all duration-200',
      isInReciteList ? 'border-l-purple-500 bg-purple-50' : 'border-l-blue-500',
    ]"
  >
    <div class="flex justify-between items-start mb-2">
      <h3 class="text-lg font-semibold text-gray-800">
        {{ chapter.Title }}
      </h3>
      <button
        @click="toggleReciteList"
        :class="[
          'px-3 py-1 rounded text-sm font-medium transition-colors whitespace-nowrap ml-2',
          isInReciteList
            ? 'bg-purple-500 hover:bg-purple-600 text-white'
            : 'bg-gray-300 hover:bg-gray-400 text-gray-800',
        ]"
        :title="isInReciteList ? '从背诵列表移除' : '添加到背诵列表'"
      >
        {{ isInReciteList ? "✓ 背诵中" : "+ 背诵" }}
      </button>
    </div>
    <p class="text-gray-700 text-sm leading-relaxed whitespace-pre-wrap">
      {{ chapter.Content }}
    </p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

const props = defineProps({
  chapter: {
    type: Object,
    required: true,
  },
  bookName: {
    type: String,
    required: true,
  },
  reciteList: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(["update-recite-list"]);

const isUpdating = ref(false);

// 计算是否在背诵列表中
const isInReciteList = computed(() => {
  const itemId = `${props.bookName}:${props.chapter.Title}`;
  return props.reciteList.some((item) => item.id === itemId);
});

// 切换背诵列表状态
const toggleReciteList = async () => {
  if (isUpdating.value) return;

  isUpdating.value = true;
  try {
    const endpoint = isInReciteList.value
      ? "/api/recite-list/remove"
      : "/api/recite-list/add";

    const response = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        book_name: props.bookName,
        chapter_title: props.chapter.Title,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || "操作失败");
    }

    // 通知父组件更新背诵列表
    emit("update-recite-list");
  } catch (err) {
    console.error("操作失败:", err);
    alert("操作失败: " + err.message);
  } finally {
    isUpdating.value = false;
  }
};
</script>
