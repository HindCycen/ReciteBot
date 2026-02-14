function getDataFromUrl() {
  const urlParams = new URLSearchParams(window.location.search);
  const dataParam = urlParams.get("data");

  if (dataParam) {
    try {
      // 解码并解析JSON数据
      const decodedData = decodeURIComponent(dataParam);
      return JSON.parse(decodedData);
    } catch (error) {
      console.error("解析URL参数失败:", error);
      return null;
    }
  }
  return null;
}

// 初始化页面
function initPage() {
  // 从URL参数获取数据
  const chaptersData = getDataFromUrl();

  if (chaptersData && Array.isArray(chaptersData)) {
    renderChapters(chaptersData);
  } else {
    // 如果没有从URL获取到数据，使用示例数据
    const sampleData = [
      {
        Title: "第一章标题",
        Content: "这是第一章的详细内容，用户可以在这里编辑文本...",
      },
      {
        Title: "第二章标题",
        Content: "这是第二章的详细内容，用户同样可以编辑这部分文本...",
      },
    ];
    renderChapters(sampleData);
  }

  // 为返回按钮添加点击事件
  document.getElementById("returnBtn").addEventListener("click", function () {
    window.history.back();
  });

  // 为保存按钮添加点击事件
  document.getElementById("saveBtn").addEventListener("click", function () {
    saveCurrentData();
  });

  // 为添加章节按钮添加点击事件
  document.getElementById("addChapterBtn").addEventListener("click", function () {
    addNewChapter();
  });
}

// 渲染章节内容
function renderChapters(chapters) {
  const container = document.getElementById("chaptersContainer");

  if (!chapters || chapters.length === 0) {
    container.innerHTML = '<div class="no-data">暂无章节数据</div>';
    return;
  }

  let html = "";
  chapters.forEach((chapter, index) => {
    html += `
            <div class="chapter" data-index="${index}">
                <div class="chapter-actions">
                    <button class="delete-chapter-btn" data-index="${index}">×</button>
                </div>
                <div class="chapter-title">
                    <input type="text" class="chapter-title-input" value="${escapeHtml(chapter.Title)}" 
                           data-field="title" data-index="${index}" placeholder="章节标题">
                </div>
                <div class="chapter-content">
                    <textarea class="chapter-content-textarea" data-field="content" 
                              data-index="${index}" placeholder="章节内容">${escapeHtml(chapter.Content)}</textarea>
                </div>
            </div>
        `;
  });

  container.innerHTML = html;

  // 添加编辑事件监听器（使用事件委托处理动态元素）
  setupEventListeners();
}

// 设置事件监听器（使用事件委托）
function setupEventListeners() {
  const container = document.getElementById("chaptersContainer");
  
  // 编辑事件委托
  container.addEventListener("input", function(event) {
    if (event.target.dataset.field) {
      handleEdit(event);
    }
  });
  
  // 删除按钮事件委托
  container.addEventListener("click", function(event) {
    if (event.target.classList.contains("delete-chapter-btn")) {
      const index = parseInt(event.target.dataset.index);
      deleteChapter(index);
    }
  });
}

// 处理编辑事件
function handleEdit(event) {
  const field = event.target.dataset.field;
  const index = parseInt(event.target.dataset.index);
  const value = event.target.value;

  // 这里可以添加保存逻辑，例如更新本地数据或发送到服务器
  console.log(`编辑章节 ${index + 1} 的 ${field}:`, value);
}

// 添加新章节
function addNewChapter() {
  const container = document.getElementById("chaptersContainer");
  
  // 移除"暂无章节数据"提示（如果存在）
  const noDataElement = container.querySelector(".no-data");
  if (noDataElement) {
    noDataElement.remove();
  }
  
  // 获取当前章节数量以确定新章节的索引
  const currentChapters = container.querySelectorAll(".chapter");
  const newIndex = currentChapters.length;
  
  // 创建新章节HTML
  const newChapterHtml = `
    <div class="chapter" data-index="${newIndex}">
        <div class="chapter-actions">
            <button class="delete-chapter-btn" data-index="${newIndex}">×</button>
        </div>
        <div class="chapter-title">
            <input type="text" class="chapter-title-input" value="新章节 ${newIndex + 1}" 
                   data-field="title" data-index="${newIndex}" placeholder="章节标题">
        </div>
        <div class="chapter-content">
            <textarea class="chapter-content-textarea" data-field="content" 
                      data-index="${newIndex}" placeholder="章节内容"></textarea>
        </div>
    </div>
  `;
  
  container.insertAdjacentHTML('beforeend', newChapterHtml);
  
  // 由于使用了事件委托，不需要重新绑定事件
}

// 删除章节
function deleteChapter(indexToDelete) {
  const container = document.getElementById("chaptersContainer");
  const chapterToRemove = container.querySelector(`.chapter[data-index="${indexToDelete}"]`);
  
  if (chapterToRemove) {
    chapterToRemove.remove();
    
    // 检查是否还有章节，如果没有则显示"暂无章节数据"
    const remainingChapters = container.querySelectorAll(".chapter");
    if (remainingChapters.length === 0) {
      container.innerHTML = '<div class="no-data">暂无章节数据</div>';
      return;
    }
    
    // 重新索引剩余的章节（可选，但为了数据一致性建议这样做）
    reindexChapters();
  }
}

// 重新索引章节（更新data-index属性）
function reindexChapters() {
  const container = document.getElementById("chaptersContainer");
  const chapters = container.querySelectorAll(".chapter");
  
  chapters.forEach((chapter, newIndex) => {
    chapter.dataset.index = newIndex;
    
    // 更新内部元素的data-index属性
    const titleInput = chapter.querySelector(".chapter-title-input");
    const contentTextarea = chapter.querySelector(".chapter-content-textarea");
    const deleteBtn = chapter.querySelector(".delete-chapter-btn");
    
    if (titleInput) titleInput.dataset.index = newIndex;
    if (contentTextarea) contentTextarea.dataset.index = newIndex;
    if (deleteBtn) deleteBtn.dataset.index = newIndex;
    
    // 更新章节标题（可选）
    if (titleInput && !titleInput.value.trim()) {
      titleInput.value = `章节 ${newIndex + 1}`;
    }
  });
}

// 获取当前编辑后的数据
function getCurrentData() {
  const bookNameInput = document.getElementById("bookName");
  const bookName = bookNameInput?.value.trim() || "未命名书籍";

  const chapters = [];
  const chapterElements = document.querySelectorAll(".chapter");

  chapterElements.forEach((chapterEl, index) => {
    const titleInput = chapterEl.querySelector(".chapter-title-input");
    const contentTextarea = chapterEl.querySelector(
      ".chapter-content-textarea",
    );

    const title = titleInput?.value.trim() || `章节 ${index + 1}`;
    const content = contentTextarea?.value.trim() || "";

    chapters.push({
      Title: title,
      Content: content,
    });
  });

  return {
    bookName: bookName,
    chapters: chapters,
  };
}

// 保存当前数据到服务器
async function saveCurrentData() {
  try {
    const currentData = getCurrentData();
    
    // 检查是否有章节数据
    if (currentData.chapters.length === 0) {
      alert("请至少添加一个章节后再保存！");
      return;
    }

    // 发送请求到后端保存API
    const response = await fetch("/api/save-book", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(currentData),
    });

    const result = await response.json();

    if (response.ok && result.success) {
      console.log("书籍已成功保存:", result.message);
      // 可以在这里添加用户提示，比如显示成功消息
      alert("书籍已成功保存为: " + result.message.split("为 ")[1]);
    } else {
      console.error("保存失败:", result.error || "未知错误");
      alert("保存失败: " + (result.error || "未知错误"));
    }
  } catch (error) {
    console.error("保存请求失败:", error);
    alert("保存请求失败，请检查网络连接");
  }
}

// 保存章节数据到服务器（保留原有函数，但不再自动调用）
async function saveChaptersToServer(chapters) {
  try {
    // 获取书籍名称
    const bookNameInput = document.getElementById("bookName");
    const bookName = bookNameInput?.value.trim() || "未命名书籍";

    // 准备要保存的数据
    const saveData = {
      bookName: bookName,
      chapters: chapters,
    };

    // 发送请求到后端保存API
    const response = await fetch("/api/save-book", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(saveData),
    });

    const result = await response.json();

    if (response.ok && result.success) {
      console.log("书籍已成功保存:", result.message);
    } else {
      console.error("保存失败:", result.error || "未知错误");
    }
  } catch (error) {
    console.error("保存请求失败:", error);
  }
}

// HTML转义函数，防止XSS攻击
function escapeHtml(text) {
  if (typeof text !== "string") return "";
  const map = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  };
  return text.replace(/[&<>"']/g, (m) => map[m]);
}

// 页面加载完成后初始化
document.addEventListener("DOMContentLoaded", initPage);