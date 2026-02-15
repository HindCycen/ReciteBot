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

    <!-- 策略选择器模态框 -->
    <StrategySelector
      :is-open="showStrategySelector"
      :chapter-title="chapter.Title"
      @confirm="handleStrategyConfirm"
      @cancel="handleStrategyCancel"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import StrategySelector from "./StrategySelector.vue";

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
const showStrategySelector = ref(false);
const selectedStrategy = ref(null);

// 计算是否在背诵列表中
const isInReciteList = computed(() => {
  const itemId = `${props.bookName}:${props.chapter.Title}`;
  return props.reciteList.some((item) => item.id === itemId);
});

// 切换背诵列表状态
const toggleReciteList = async () => {
  if (isUpdating.value) return;

  // 如果是移除操作
  if (isInReciteList.value) {
    await removeFromReciteList();
    return;
  }

  // 如果是添加操作，先显示策略选择器
  showStrategySelector.value = true;
};

// 从背诵列表移除
const removeFromReciteList = async () => {
  isUpdating.value = true;
  try {
    const response = await fetch("/api/recite-list/remove", {
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
      throw new Error(errorData.error || "移除失败");
    }

    emit("update-recite-list");
  } catch (err) {
    console.error("移除失败:", err);
    alert("移除失败: " + err.message);
  } finally {
    isUpdating.value = false;
  }
};

// 处理策略选择确认
const handleStrategyConfirm = async (strategy) => {
  isUpdating.value = true;
  try {
    const response = await fetch("/api/recite-list/add", {
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
      throw new Error(errorData.error || "添加失败");
    }

    // 显示成功提示
    const data = await response.json();
    if (data.success) {
      alert(
        `✓ 已添加到背诵列表\n策略: ${strategy}\n周期: ${data.review_cycle_days} 天`,
      );
    }

    emit("update-recite-list");
    showStrategySelector.value = false;
  } catch (err) {
    console.error("添加失败:", err);
    alert("添加失败: " + err.message);
  } finally {
    isUpdating.value = false;
  }
};

// 处理策略选择取消
const handleStrategyCancel = () => {
  showStrategySelector.value = false;
  selectedStrategy.value = null;
};
</script>
