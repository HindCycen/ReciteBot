<template>
  <div
    :class="[
      'relative group bg-gray-50 border-l-4 rounded-lg p-4 hover:-translate-y-1 hover:shadow-lg transition-all duration-200',
      isInReciteList ? 'border-l-purple-500 bg-purple-50' : 'border-l-blue-500',
    ]"
  >
    <!-- 删除和移动按钮区域 -->
    <div
      class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 flex gap-1 transition-opacity"
    >
      <!-- 向上移动按钮 -->
      <button
        v-if="!isFirst"
        @click="$emit('move-up', index)"
        class="bg-blue-500 hover:bg-blue-600 text-white rounded w-6 h-6 flex items-center justify-center transition-colors"
        title="上移"
      >
        ↑
      </button>

      <!-- 向下移动按钮 -->
      <button
        v-if="!isLast"
        @click="$emit('move-down', index)"
        class="bg-blue-500 hover:bg-blue-600 text-white rounded w-6 h-6 flex items-center justify-center transition-colors"
        title="下移"
      >
        ↓
      </button>

      <!-- 删除按钮 -->
      <button
        @click="$emit('delete', index)"
        class="bg-red-500 hover:bg-red-600 text-white rounded-full w-6 h-6 flex items-center justify-center transition-colors"
        title="删除"
      >
        ×
      </button>
    </div>

    <div class="flex justify-between items-start gap-2 mb-3">
      <input
        v-model="chapter.Title"
        type="text"
        class="text-xl font-semibold flex-1 p-1 border-b border-gray-300 focus:outline-none focus:border-blue-500"
        placeholder="章节标题"
      />
      <button
        @click="toggleReciteList"
        :class="[
          'px-3 py-1 rounded text-sm font-medium transition-colors whitespace-nowrap',
          isInReciteList
            ? 'bg-purple-500 hover:bg-purple-600 text-white'
            : 'bg-gray-300 hover:bg-gray-400 text-gray-800',
        ]"
        :title="isInReciteList ? '从背诵列表移除' : '添加到背诵列表'"
        :disabled="isUpdating"
      >
        {{ isInReciteList ? "✓ 背诵中" : "+ 背诵" }}
      </button>
    </div>

    <textarea
      v-model="chapter.Content"
      class="min-h-[150px] resize-y w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      placeholder="章节内容..."
    ></textarea>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const props = defineProps({
  chapter: {
    type: Object,
    required: true,
  },
  index: {
    type: Number,
    required: true,
  },
  isFirst: {
    type: Boolean,
    default: false,
  },
  isLast: {
    type: Boolean,
    default: false,
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

const emit = defineEmits([
  "delete",
  "move-up",
  "move-down",
  "update-recite-list",
]);

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
