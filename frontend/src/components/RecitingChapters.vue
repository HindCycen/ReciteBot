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
              type="button"
              @click="showMode = 'due'"
              :class="[
                'px-4 py-2 rounded-lg transition-colors duration-200',
                showMode === 'due'
                  ? 'bg-green-500 hover:bg-green-600 text-white'
                  : 'bg-gray-300 hover:bg-gray-400 text-gray-800',
              ]"
            >
              📚 应该复习 ({{ dueCounts }})
            </button>
            <button
              type="button"
              @click="showMode = 'waiting'"
              :class="[
                'px-4 py-2 rounded-lg transition-colors duration-200',
                showMode === 'waiting'
                  ? 'bg-orange-500 hover:bg-orange-600 text-white'
                  : 'bg-gray-300 hover:bg-gray-400 text-gray-800',
              ]"
            >
              ⏳ 等待中 ({{ waitingCounts }})
            </button>
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
        <div v-else-if="displayBooks.length === 0" class="text-center py-12">
          <p class="text-gray-500 text-lg">
            {{ showMode === "due" ? "暂无应该复习的章节" : "暂无等待中的章节" }}
          </p>
          <p class="text-gray-400 mt-2">
            {{
              showMode === "due"
                ? "所有章节都已背过，继续加油！"
                : '请在「所有章节浏览」中标记章节为"正在背诵"'
            }}
          </p>
        </div>

        <!-- 按书名分组的背诵章节列表 -->
        <div v-else class="space-y-10">
          <div
            v-for="book in displayBooks"
            :key="book.book_name"
            :class="[
              'border rounded-lg overflow-hidden',
              showMode === 'due'
                ? 'border-green-200 bg-green-50'
                : 'border-orange-200 bg-orange-50',
            ]"
          >
            <!-- 书名标题 -->
            <div
              :class="[
                'text-white px-6 py-4 sticky top-0',
                showMode === 'due' ? 'bg-green-500' : 'bg-orange-500',
              ]"
            >
              <h2 class="text-2xl font-bold">{{ book.book_name }}</h2>
              <p
                :class="
                  showMode === 'due' ? 'text-green-100' : 'text-orange-100'
                "
                class="text-sm mt-1"
              >
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
                  @memorized="handleMemorized"
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
const allBooks = ref([]);
const loading = ref(false);
const error = ref("");
const showMode = ref("due"); // "due" 或 "waiting"

// 计算应该复习的总数
const dueCounts = computed(() => {
  return books.value.reduce((sum, book) => sum + book.chapters.length, 0);
});

// 计算等待中的总数
const waitingCounts = computed(() => {
  return (
    allBooks.value.reduce((sum, book) => sum + book.chapters.length, 0) -
    dueCounts.value
  );
});

// 计算总章节数
const totalChapters = computed(() => {
  return dueCounts.value + waitingCounts.value;
});

// 根据模式显示的书籍
const displayBooks = computed(() => {
  return showMode.value === "due" ? books.value : getWaitingBooks();
});

// 获取等待中的书籍
const getWaitingBooks = () => {
  if (allBooks.value.length === 0) return [];

  const result = [];
  for (const allBook of allBooks.value) {
    // 找到同名的应该复习书籍
    const dueBook = books.value.find((b) => b.book_name === allBook.book_name);

    if (!dueBook) {
      // 整个书籍都是等待中
      result.push(allBook);
    } else {
      // 找出这个书籍中等待中的章节
      const waitingChapters = allBook.chapters.filter(
        (allChapter) =>
          !dueBook.chapters.some(
            (dueChapter) => dueChapter.Title === allChapter.Title,
          ),
      );

      if (waitingChapters.length > 0) {
        result.push({
          book_name: allBook.book_name,
          chapters: waitingChapters,
        });
      }
    }
  }
  return result;
};

// 获取应该背诵的章节
const fetchRecitingChapters = async () => {
  loading.value = true;
  error.value = "";

  try {
    const [dueResponse, allResponse] = await Promise.all([
      fetch("/api/reciting-chapters"),
      fetch("/api/all-reciting-chapters"),
    ]);

    if (!dueResponse.ok) {
      const errorData = await dueResponse.json().catch(() => ({}));
      throw new Error(errorData.error || "获取背诵章节失败");
    }

    if (!allResponse.ok) {
      const errorData = await allResponse.json().catch(() => ({}));
      throw new Error(errorData.error || "获取所有背诵章节失败");
    }

    const dueData = await dueResponse.json();
    const allData = await allResponse.json();

    books.value = dueData;
    allBooks.value = allData;
  } catch (err) {
    console.error("获取背诵章节失败:", err);
    error.value = err.message || "获取背诵章节失败";
  } finally {
    loading.value = false;
  }
};

// 处理背过了
const handleMemorized = async () => {
  await fetchRecitingChapters();
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
