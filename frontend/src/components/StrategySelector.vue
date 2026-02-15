<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
  >
    <div
      class="bg-white rounded-lg shadow-lg max-w-md w-full p-6 max-h-96 overflow-y-auto"
    >
      <h2 class="text-2xl font-bold mb-4 text-gray-800">选择背诵周期</h2>
      <p class="text-gray-600 mb-6">
        为
        <span class="font-semibold">{{ chapterTitle }}</span> 选择一个复习周期
      </p>

      <div v-if="loading" class="text-center py-4">
        <p class="text-gray-500">加载中...</p>
      </div>

      <div v-else-if="error" class="text-center py-4 text-red-500">
        <p>{{ error }}</p>
      </div>

      <div v-else class="space-y-3 mb-6">
        <button
          v-for="strategy in strategies"
          :key="strategy.name"
          @click="selectStrategy(strategy.name)"
          :class="[
            'w-full p-4 rounded-lg border-2 text-left transition-all',
            selectedStrategy === strategy.name
              ? 'border-blue-500 bg-blue-50'
              : 'border-gray-200 bg-white hover:border-gray-300',
          ]"
        >
          <div class="flex items-start justify-between">
            <div class="flex-1">
              <h3 class="font-semibold text-gray-800">{{ strategy.label }}</h3>
              <p class="text-sm text-gray-600 mt-1">
                {{ strategy.description }}
              </p>
              <p class="text-xs text-gray-500 mt-2">
                📅 约 {{ strategy.cycle_days }} 天完成 | 🔄
                {{ strategy.total_reviews }}
                次复习
              </p>
            </div>
            <div
              v-if="selectedStrategy === strategy.name"
              class="ml-3 flex-shrink-0 text-blue-500"
            >
              ✓
            </div>
          </div>
        </button>
      </div>

      <div class="flex gap-2">
        <button
          @click="cancel"
          class="flex-1 px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-lg font-medium transition-colors"
        >
          取消
        </button>
        <button
          @click="confirm"
          :disabled="!selectedStrategy || isConfirming"
          :class="[
            'flex-1 px-4 py-2 rounded-lg font-medium transition-colors',
            selectedStrategy && !isConfirming
              ? 'bg-blue-500 hover:bg-blue-600 text-white cursor-pointer'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed',
          ]"
        >
          {{ isConfirming ? "处理中..." : "确认" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true,
  },
  chapterTitle: {
    type: String,
    required: true,
  },
});

const emit = defineEmits(["confirm", "cancel"]);

const strategies = ref([]);
const selectedStrategy = ref(null);
const loading = ref(false);
const error = ref("");
const isConfirming = ref(false);

const strategyLabels = {
  aggressive: "⚡ 激进策略（7天快速掌握）",
  balanced: "⚙️ 均衡策略（14天标准学习）",
  standard: "📚 标准策略（30天深度记忆）",
};

// 获取复习策略
const fetchStrategies = async () => {
  loading.value = true;
  error.value = "";
  try {
    const response = await fetch("/api/review-strategies");
    if (!response.ok) {
      throw new Error("获取复习策略失败");
    }
    const data = await response.json();
    strategies.value = data.strategies.map((strategy) => ({
      ...strategy,
      label: strategyLabels[strategy.name] || strategy.name,
    }));
    // 默认选择标准策略
    selectedStrategy.value = data.default_strategy;
  } catch (err) {
    console.error("获取复习策略失败:", err);
    error.value = "获取复习策略失败，请重试";
  } finally {
    loading.value = false;
  }
};

const selectStrategy = (strategyName) => {
  selectedStrategy.value = strategyName;
};

const confirm = async () => {
  if (!selectedStrategy.value) return;
  isConfirming.value = true;
  try {
    emit("confirm", selectedStrategy.value);
  } finally {
    isConfirming.value = false;
  }
};

const cancel = () => {
  selectedStrategy.value = null;
  emit("cancel");
};

// 监听 isOpen 变化
watch(
  () => props.isOpen,
  (newVal) => {
    if (newVal) {
      fetchStrategies();
    } else {
      selectedStrategy.value = null;
    }
  },
);
</script>
