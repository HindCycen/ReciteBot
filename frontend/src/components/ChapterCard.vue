<template>
  <div
    :class="[
      'relative group bg-gray-50 border-l-4 border-blue-500 rounded-lg p-4 hover:-translate-y-1 hover:shadow-lg transition-all duration-200'
    ]"
  >
    <!-- 删除和移动按钮区域 -->
    <div class="absolute top-2 right-2 opacity-0 group-hover:opacity-100 flex gap-1 transition-opacity">
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

    <input
      v-model="chapter.Title"
      type="text"
      class="text-xl font-semibold w-full p-1 mb-3 border-b border-gray-300 focus:outline-none focus:border-blue-500"
      placeholder="章节标题"
    />

    <textarea
      v-model="chapter.Content"
      class="min-h-[150px] resize-y w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
      placeholder="章节内容..."
    ></textarea>
  </div>
</template>

<script setup>
defineProps({
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
});

defineEmits(["delete", "move-up", "move-down"]);
</script>
