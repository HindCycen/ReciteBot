const API_BASE = ""; // 若后端同域可留空，否则填写完整地址

export async function saveBook(bookName, chapters) {
  const response = await fetch(`${API_BASE}/api/save-book`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ bookName, chapters }),
  });
  if (!response.ok) {
    const error = await response.text();
    throw new Error(error || "保存失败");
  }
  return response.json();
}

export async function processText(text) {
  const response = await fetch(`${API_BASE}/api/process`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.error || "处理失败");
  }
  return response.json();
}
