<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <div class="max-w-6xl mx-auto">
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex justify-between items-center mb-8">
          <h1 class="text-3xl font-bold">所有章节浏览</h1>
          <button
            @click="goBackToInput"
            class="bg-gray-400 hover:bg-gray-500 text-white px-4 py-2 rounded-lg transition-colors duration-200"
            type="button"
          >
            返回
          </button>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="text-center py-8">
          <p class="text-gray-500 text-lg">加载中...</p>
        </div>

        <!-- 错误状态 -->
        <div v-else-if="error" class="text-center py-8 text-red-500">
          <p>{{ error }}</p>
        </div>

        <!-- 空状态 -->
        <div v-else-if="books.length === 0" class="text-center py-12">
          <p class="text-gray-500 text-lg">暂无章节数据</p>
          <p class="text-gray-400 mt-2">请先创建并保存书籍</p>
        </div>

        <!-- 按书名分组的章节列表 -->
        <div v-else class="space-y-10">
          <div
            v-for="book in books"
            :key="book.book_name"
            class="border border-gray-200 rounded-lg overflow-hidden"
          >
            <!-- 书名标题 -->
            <div class="bg-blue-500 text-white px-6 py-4 sticky top-0">
              <h2 class="text-2xl font-bold">{{ book.book_name }}</h2>
              <p class="text-blue-100 text-sm mt-1">
                共 {{ book.chapters.length }} 个章节
              </p>
            </div>

            <!-- 书内章节列表 -->
            <div class="bg-white p-6">
              <div class="grid grid-cols-1 gap-4">
                <ReadOnlyChapterCard
                  v-for="(chapter, index) in book.chapters"
                  :key="index"
                  :chapter="chapter"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import ReadOnlyChapterCard from "./ReadOnlyChapterCard.vue";

const emit = defineEmits(["go-back"]);

const books = ref([]);
const loading = ref(false);
const error = ref("");

// 获取所有章节
const fetchAllChapters = async () => {
  loading.value = true;
  error.value = "";

  try {
    const response = await fetch("/api/all-chapters");

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || "获取章节数据失败");
    }

    const data = await response.json();
    books.value = data;
  } catch (err) {
    console.error("获取所有章节失败:", err);
    error.value = err.message || "获取所有章节失败";
  } finally {
    loading.value = false;
  }
};

// 返回上一页
const goBackToInput = () => {
  emit("go-back");
};

// 组件挂载时获取数据
onMounted(() => {
  fetchAllChapters();
});
</script>
