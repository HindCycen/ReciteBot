<template>
  <div class="min-h-screen bg-gray-50 p-8">
    <div class="max-w-4xl mx-auto">
      <!-- 文本输入页面 -->
      <div
        v-if="currentPage === 'input'"
        class="bg-white rounded-lg shadow-md p-6"
      >
        <h1 class="text-3xl font-bold text-center mb-8">
          ReciteBot - 文本处理
        </h1>

        <div class="mb-6">
          <label class="block text-gray-700 font-medium mb-2"
            >请输入要处理的文本：</label
          >
          <textarea
            v-model="inputText"
            class="w-full min-h-[300px] p-4 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y"
            placeholder="在此输入您的文本内容..."
          ></textarea>
        </div>

        <div class="flex justify-center space-x-4">
          <button
            @click="processText"
            :disabled="processing || !inputText.trim()"
            class="bg-blue-500 hover:bg-blue-600 disabled:bg-blue-300 text-white px-6 py-2 rounded-lg transition-colors duration-200"
            type="button"
          >
            {{ processing ? "处理中..." : "提交给AI处理" }}
          </button>
          <button
            @click="goToBookList"
            class="bg-gray-400 hover:bg-gray-500 text-white px-6 py-2 rounded-lg transition-colors duration-200"
            type="button"
          >
            我的书籍
          </button>
          <button
            @click="goToAllChapters"
            class="bg-purple-500 hover:bg-purple-600 text-white px-6 py-2 rounded-lg transition-colors duration-200"
            type="button"
          >
            所有章节
          </button>
          <button
            @click="goToRecitingChapters"
            class="bg-pink-500 hover:bg-pink-600 text-white px-6 py-2 rounded-lg transition-colors duration-200"
            type="button"
          >
            正在背诵
          </button>
        </div>

        <div v-if="error" class="mt-4 text-red-500 text-center">
          {{ error }}
        </div>
      </div>

      <!-- 章节编辑页面 -->
      <div
        v-else-if="currentPage === 'editor'"
        class="bg-white rounded-lg shadow-md p-6"
      >
        <h1 class="text-3xl font-bold text-center mb-8">
          ReciteBot - 结果展示
        </h1>

        <!-- 书籍名称区域 -->
        <div class="mb-6">
          <label class="block text-gray-700 font-medium mb-2">书籍名称</label>
          <input
            v-model="bookName"
            type="text"
            class="w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="请输入书籍名称"
          />
        </div>

        <!-- 章节操作区域 -->
        <div class="mb-6">
          <button
            @click="addChapter"
            class="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg transition-colors duration-200"
            type="button"
          >
            + 添加新章节
          </button>
        </div>

        <!-- 章节容器区域 -->
        <div class="space-y-4 mb-8">
          <ChapterCard
            v-for="(chapter, index) in chapters"
            :key="index"
            :chapter="chapter"
            :index="index"
            :is-first="index === 0"
            :is-last="index === chapters.length - 1"
            :book-name="bookName"
            :recite-list="reciteList"
            @delete="deleteChapter"
            @move-up="moveChapterUp"
            @move-down="moveChapterDown"
            @update-recite-list="fetchReciteList"
          />

          <!-- 空状态提示 -->
          <div
            v-if="chapters.length === 0"
            class="text-center text-gray-500 py-8"
          >
            暂无章节数据
          </div>
        </div>

        <!-- 底部操作按钮 -->
        <div class="flex justify-center space-x-4">
          <button
            @click="handleSave"
            class="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded-lg transition-colors duration-200"
            type="button"
          >
            保存到文件
          </button>
          <button
            @click="goBackToInput"
            class="bg-gray-400 hover:bg-gray-500 text-white px-6 py-2 rounded-lg transition-colors duration-200"
            type="button"
          >
            返回编辑文本
          </button>
          <button
            @click="goToBookList"
            class="bg-gray-400 hover:bg-gray-500 text-white px-6 py-2 rounded-lg transition-colors duration-200"
            type="button"
          >
            我的书籍
          </button>
        </div>
      </div>

      <!-- 书籍列表页面 -->
      <BookList
        v-else-if="currentPage === 'book-list'"
        @load-book="loadBookContent"
        @go-back="goBackToInput"
        @create-book="createNewBook"
        @view-all-chapters="goToAllChapters"
        @view-reciting-chapters="goToRecitingChapters"
      />

      <!-- 所有章节浏览页面 -->
      <AllChapters
        v-else-if="currentPage === 'all-chapters'"
        @go-back="goBackToInput"
        @go-to-reciting-chapters="goToRecitingChapters"
      />

      <!-- 正在背诵的章节页面 -->
      <RecitingChapters
        v-else-if="currentPage === 'reciting-chapters'"
        @go-back="goBackToInput"
        @go-to-all-chapters="goToAllChapters"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import ChapterCard from "./components/ChapterCard.vue";
import BookList from "./components/BookList.vue";
import AllChapters from "./components/AllChapters.vue";
import RecitingChapters from "./components/RecitingChapters.vue";
import { saveBook, getBookContent } from "./api";

// 页面状态
const currentPage = ref("input");

// 文本输入页面数据
const inputText = ref("");
const processing = ref(false);
const error = ref("");

// 章节编辑页面数据
const bookName = ref("未命名书籍");
const chapters = ref([]);

// 背诵列表
const reciteList = ref([]);

// 获取背诵列表
const fetchReciteList = async () => {
  try {
    const response = await fetch("/api/recite-list");
    if (response.ok) {
      reciteList.value = await response.json();
    }
  } catch (err) {
    console.error("获取背诵列表失败:", err);
  }
};

// 处理文本
const processText = async () => {
  if (!inputText.value.trim()) return;

  processing.value = true;
  error.value = "";

  try {
    const response = await fetch("/api/process", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: inputText.value }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.error || "处理失败");
    }

    const result = await response.json();

    // 验证结果格式
    if (!Array.isArray(result) || result.length === 0) {
      throw new Error("AI返回的数据格式不正确");
    }

    // 验证每个章节都有 Title 和 Content
    for (const chapter of result) {
      if (!chapter.Title || !chapter.Content) {
        throw new Error("AI返回的章节数据缺少必要字段");
      }
    }

    // 切换到编辑页面
    chapters.value = result;
    currentPage.value = "editor";
  } catch (err) {
    console.error("处理文本失败:", err);
    error.value = err.message || "处理失败，请稍后重试";
  } finally {
    processing.value = false;
  }
};

// 添加章节
const addChapter = () => {
  chapters.value.push({
    Title: `新章节 ${chapters.value.length + 1}`,
    Content: "",
  });
};

// 删除章节
const deleteChapter = (index) => {
  chapters.value.splice(index, 1);
};

// 移动章节
const moveChapterUp = (index) => {
  if (index > 0) {
    const temp = chapters.value[index];
    chapters.value[index] = chapters.value[index - 1];
    chapters.value[index - 1] = temp;
  }
};

const moveChapterDown = (index) => {
  if (index < chapters.value.length - 1) {
    const temp = chapters.value[index];
    chapters.value[index] = chapters.value[index + 1];
    chapters.value[index + 1] = temp;
  }
};

// 保存逻辑
const handleSave = async () => {
  if (chapters.value.length === 0) {
    alert("请至少添加一个章节");
    return;
  }
  const name = bookName.value.trim() || "未命名书籍";
  try {
    const result = await saveBook(name, chapters.value);
    alert("保存成功！");
  } catch (err) {
    alert("保存失败：" + err.message);
  }
};

// 返回文本输入页面
const goBackToInput = () => {
  currentPage.value = "input";
};

// 跳转到书籍列表页面
const goToBookList = () => {
  currentPage.value = "book-list";
};

// 加载指定书籍的内容
const loadBookContent = async (filename) => {
  try {
    const bookData = await getBookContent(filename);
    bookName.value = bookData.name;
    chapters.value = bookData.content;
    currentPage.value = "editor";
    await fetchReciteList();
  } catch (err) {
    alert("加载书籍失败：" + err.message);
  }
};

// 创建新书籍
const createNewBook = () => {
  bookName.value = "未命名书籍";
  chapters.value = [];
  currentPage.value = "editor";
  fetchReciteList();
};

// 跳转到所有章节浏览页面
const goToAllChapters = () => {
  currentPage.value = "all-chapters";
};

// 跳转到正在背诵的章节页面
const goToRecitingChapters = () => {
  currentPage.value = "reciting-chapters";
};

// 组件挂载时获取背诵列表
onMounted(() => {
  fetchReciteList();
});
</script>
