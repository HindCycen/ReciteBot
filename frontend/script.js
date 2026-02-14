// ReciteBot - AI 文本分章工具的JavaScript逻辑
// 喵。

async function processText() {
  const inputText = document.getElementById("textInput").value.trim();
  const processBtn = document.getElementById("processBtn");
  const loadingDiv = document.getElementById("loading");
  const resultDiv = document.getElementById("result");
  const errorDiv = document.getElementById("error");

  // 输入验证
  if (!inputText) {
    showError("请输入文本内容！");
    return;
  }

  // 禁用按钮并显示加载状态
  processBtn.disabled = true;
  loadingDiv.style.display = "block";
  resultDiv.style.display = "none";
  errorDiv.style.display = "none";

  try {
    // 这里需要后端API端点来处理请求
    // 由于原ai_call.py是命令行脚本，我们需要创建一个Web API接口
    const response = await fetch("/api/process", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: inputText }),
    });

    if (!response.ok) {
      throw new Error(`服务器错误: ${response.status}`);
    }

    const result = await response.json();
    // 不再显示JSON，而是跳转到result.html页面
    redirectToResultPage(result);
  } catch (error) {
    console.error("处理失败:", error);
    showError("处理失败: " + error.message);
  } finally {
    // 恢复按钮状态
    processBtn.disabled = false;
    loadingDiv.style.display = "none";
  }
}

function redirectToResultPage(result) {
  // 将结果数据编码为URL参数
  const encodedData = encodeURIComponent(JSON.stringify(result));
  // 跳转到result.html并传递数据
  window.location.href = `result.html?data=${encodedData}`;
}

function showError(message) {
  const errorDiv = document.getElementById("error");
  errorDiv.textContent = message;
  errorDiv.style.display = "block";
}

// 允许按Enter+Ctrl/Cmd提交
document.getElementById("textInput").addEventListener("keydown", function (e) {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
    e.preventDefault();
    processText();
  }
});
