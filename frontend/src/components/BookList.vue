<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <div class="max-w-4xl mx-auto">
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex justify-between items-center mb-8">
          <h1 class="text-3xl font-bold">我的书籍</h1>
          <div class="space-x-2">
            <button
              type="button"
              @click="createNewBook"
              class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-colors duration-200"
            >
              + 新建书籍
            </button>
            <button
              type="button"
              @click="viewAllChapters"
              class="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-lg transition-colors duration-200"
            >
              所有章节
            </button>
            <button
              type="button"
              @click="viewRecitingChapters"
              class="bg-pink-500 hover:bg-pink-600 text-white px-4 py-2 rounded-lg transition-colors duration-200"
            >
              正在背诵
            </button>
            <button
              type="button"
              @click="goBackToInput"
              class="bg-gray-400 hover:bg-gray-500 text-white px-4 py-2 rounded-lg transition-colors duration-200"
            >
              返回AI处理
            </button>
          </div>
        </div>

        <!-- 书籍列表 -->
        <div v-if="books.length > 0" class="space-y-4">
          <div
            v-for="book in books"
            :key="book.filename"
            @click="loadBook(book.filename)"
            class="border border-gray-200 rounded-lg p-4 hover:bg-blue-50 cursor-pointer transition-colors duration-200"
          >
            <div class="flex justify-between items-center">
              <div class="font-medium text-lg">{{ book.name }}</div>
              <div class="text-sm text-gray-500">{{ book.modified }}</div>
            </div>
          </div>
        </div>

        <!-- 空状态 -->
        <div v-else class="text-center py-12">
          <p class="text-gray-500 text-lg">暂无书籍</p>
          <p class="text-gray-400 mt-2">保存的书籍将显示在这里</p>
          <button
            type="button"
            @click="createNewBook"
            class="mt-6 bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded-lg transition-colors duration-200"
          >
            创建你的第一本书籍
          </button>
        </div>

        <!-- 加载状态 -->
        <div v-if="loading" class="text-center py-4">
          <p class="text-gray-500">加载中...</p>
        </div>

        <!-- 错误状态 -->
        <div v-if="error" class="text-center py-4 text-red-500">
          {{ error }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { getBooksList } from "../api";

// 定义 emits
const emit = defineEmits([
  "load-book",
  "go-back",
  "create-book",
  "view-all-chapters",
  "view-reciting-chapters",
]);

// 数据
const books = ref([]);
const loading = ref(false);
const error = ref("");

// 获取书籍列表
const fetchBooks = async () => {
  loading.value = true;
  error.value = "";

  try {
    const booksData = await getBooksList();
    books.value = booksData;
  } catch (err) {
    console.error("获取书籍列表失败:", err);
    error.value = err.message || "获取书籍列表失败";
  } finally {
    loading.value = false;
  }
};

// 加载指定书籍
const loadBook = (filename) => {
  emit("load-book", filename);
};

// 返回 AI 处理页面
const goBackToInput = () => {
  emit("go-back");
};

// 创建新书籍
const createNewBook = () => {
  emit("create-book");
};

// 查看所有章节
const viewAllChapters = () => {
  emit("view-all-chapters");
};

// 查看正在背诵的章节
const viewRecitingChapters = () => {
  emit("view-reciting-chapters");
};

// 组件挂载时获取书籍列表
onMounted(() => {
  fetchBooks();
});
</script>
