<template>
  <div
    class="bg-purple-50 border-l-4 border-l-purple-500 rounded-lg p-4 hover:shadow-md transition-all duration-200"
  >
    <div class="flex justify-between items-start mb-3">
      <div class="flex-1">
        <h3 class="text-lg font-semibold text-gray-800">
          {{ chapter.Title }}
        </h3>
        <p class="text-xs text-gray-500 mt-1">
          添加于: {{ formatDate(chapter.added_at) }}
        </p>
        <p v-if="chapter.review_count > 0" class="text-xs text-gray-600 mt-1">
          已复习 {{ chapter.review_count }} 次 | 下次复习:
          {{ formatDate(chapter.next_review_at) }}
        </p>
      </div>
      <div class="flex gap-2 ml-2">
        <button
          @click="showStrategyChanger = true"
          class="px-3 py-1 rounded text-sm font-medium transition-colors whitespace-nowrap bg-blue-500 hover:bg-blue-600 text-white"
          title="修改复习周期"
          :disabled="isUpdating"
        >
          🔄 周期
        </button>
        <button
          @click="markAsMemorized"
          class="px-3 py-1 rounded text-sm font-medium transition-colors whitespace-nowrap bg-green-500 hover:bg-green-600 text-white"
          title="标记为背过了"
          :disabled="isUpdating"
        >
          {{ isUpdating ? "处理中..." : "✓ 背过了" }}
        </button>
      </div>
    </div>
    <p class="text-gray-700 text-sm leading-relaxed whitespace-pre-wrap">
      {{ chapter.Content }}
    </p>

    <!-- 策略修改模态框 -->
    <StrategyChanger
      :is-open="showStrategyChanger"
      :chapter-title="chapter.Title"
      :current-strategy="chapter.strategy || 'standard'"
      @confirm="handleStrategyChange"
      @cancel="showStrategyChanger = false"
    />
  </div>
</template>

<script setup>
import { ref } from "vue";
import StrategyChanger from "./StrategyChanger.vue";

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

const emit = defineEmits(["memorized"]);

const isUpdating = ref(false);
const showStrategyChanger = ref(false);

// 格式化日期
const formatDate = (dateString) => {
  try {
    const date = new Date(dateString);
    return date.toLocaleString("zh-CN");
  } catch {
    return dateString;
  }
};

// 标记为背过了
const markAsMemorized = async () => {
  if (isUpdating.value) return;

  isUpdating.value = true;
  try {
    const response = await fetch("/api/recite-list/memorized", {
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
      throw new Error(errorData.error || "标记失败");
    }

    const result = await response.json();
    alert(`已标记为背过了！下次复习时间: ${formatDate(result.next_review_at)}`);

    // 通知父组件刷新列表
    emit("memorized");
  } catch (err) {
    console.error("标记章节失败:", err);
    alert("标记失败: " + err.message);
  } finally {
    isUpdating.value = false;
  }
};

// 处理策略修改
const handleStrategyChange = async (strategy) => {
  isUpdating.value = true;
  try {
    const response = await fetch("/api/recite-list/change-strategy", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        book_name: props.bookName,
        chapter_title: props.chapter.Title,
        strategy: strategy,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || "修改策略失败");
    }

    const result = await response.json();
    alert(
      `✓ 已修改复习策略\n新策略: ${strategy}\n新周期: ${result.review_cycle_days} 天\n下次复习: ${formatDate(result.next_review_at)}`,
    );

    showStrategyChanger.value = false;
    // 通知父组件刷新列表
    emit("memorized");
  } catch (err) {
    console.error("修改策略失败:", err);
    alert("修改策略失败: " + err.message);
  } finally {
    isUpdating.value = false;
  }
};
</script>
