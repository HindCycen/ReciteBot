<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <div class="max-w-6xl mx-auto">
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex justify-between items-center mb-8">
          <div>
            <h1 class="text-3xl font-bold">正在背诵的章节</h1>
            <p v-if="!loading && books.length > 0" class="text-gray-500 mt-2">
              共 {{ totalChapters }} 个章节
            </p>
          </div>
          <div class="flex gap-2">
            <button
              @click="goToAllChapters"
              class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg transition-colors duration-200"
              type="button"
            >
              浏览所有章节
            </button>
            <button
              @click="goBackToInput"
              class="bg-gray-400 hover:bg-gray-500 text-white px-4 py-2 rounded-lg transition-colors duration-200"
              type="button"
            >
              返回
            </button>
          </div>
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
          <p class="text-gray-500 text-lg">暂无背诵章节</p>
          <p class="text-gray-400 mt-2">
            请在「所有章节浏览」中标记章节为"正在背诵"
          </p>
        </div>

        <!-- 按书名分组的背诵章节列表 -->
        <div v-else class="space-y-10">
          <div
            v-for="book in books"
            :key="book.book_name"
            class="border border-purple-200 rounded-lg overflow-hidden"
          >
            <!-- 书名标题 -->
            <div class="bg-purple-500 text-white px-6 py-4 sticky top-0">
              <h2 class="text-2xl font-bold">{{ book.book_name }}</h2>
              <p class="text-purple-100 text-sm mt-1">
                共 {{ book.chapters.length }} 个章节
              </p>
            </div>

            <!-- 书内章节列表 -->
            <div class="bg-white p-6">
              <div class="grid grid-cols-1 gap-4">
                <RecitingChapterCard
                  v-for="(chapter, index) in book.chapters"
                  :key="index"
                  :chapter="chapter"
                  :book-name="book.book_name"
                  @remove-chapter="removeChapter"
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
import { ref, computed, onMounted } from "vue";
import RecitingChapterCard from "./RecitingChapterCard.vue";

const emit = defineEmits(["go-back", "go-to-all-chapters"]);

const books = ref([]);
const loading = ref(false);
const error = ref("");

// 计算总章节数
const totalChapters = computed(() => {
  return books.value.reduce((sum, book) => sum + book.chapters.length, 0);
});

// 获取背诵中的章节
const fetchRecitingChapters = async () => {
  loading.value = true;
  error.value = "";

  try {
    const response = await fetch("/api/reciting-chapters");

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || "获取背诵章节失败");
    }

    const data = await response.json();
    books.value = data;
  } catch (err) {
    console.error("获取背诵章节失败:", err);
    error.value = err.message || "获取背诵章节失败";
  } finally {
    loading.value = false;
  }
};

// 移除章节
const removeChapter = async (bookName, chapterTitle) => {
  try {
    const response = await fetch("/api/recite-list/remove", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        book_name: bookName,
        chapter_title: chapterTitle,
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || "移除失败");
    }

    // 重新加载分页数据
    await fetchRecitingChapters();
  } catch (err) {
    console.error("移除章节失败:", err);
    alert("移除失败: " + err.message);
  }
};

// 返回上一页
const goBackToInput = () => {
  emit("go-back");
};

// 跳转到所有章节浏览页面
const goToAllChapters = () => {
  emit("go-to-all-chapters");
};

// 组件挂载时获取数据
onMounted(() => {
  fetchRecitingChapters();
});
</script>
