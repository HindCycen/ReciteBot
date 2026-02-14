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

  // 添加编辑事件监听器
  addEditEventListeners();
}

// 添加编辑事件监听器
function addEditEventListeners() {
  const inputs = document.querySelectorAll("[data-field]");
  inputs.forEach((input) => {
    input.addEventListener("input", handleEdit);
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
