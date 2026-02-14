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
    displayResult(result);
  } catch (error) {
    console.error("处理失败:", error);
    showError("处理失败: " + error.message);
  } finally {
    // 恢复按钮状态
    processBtn.disabled = false;
    loadingDiv.style.display = "none";
  }
}

function displayResult(result) {
  const resultDiv = document.getElementById("result");
  try {
    // 格式化JSON输出以便阅读
    const formattedResult = JSON.stringify(result, null, 2);
    resultDiv.textContent = formattedResult;
    resultDiv.style.display = "block";
  } catch (e) {
    resultDiv.textContent = JSON.stringify(result);
    resultDiv.style.display = "block";
  }
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
