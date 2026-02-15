# GitHub Release 使用指南

本指南说明如何下载、安装和使用从 GitHub Release 构建的项目文件。

## 📦 Release 文件说明

### 生成的文件类型

每个 Release 会生成多个平台的构建文件：

| 文件名                   | 平台       | 格式     | 大小 | 解压工具           |
| ------------------------ | ---------- | -------- | ---- | ------------------ |
| `recitebot-linux.tar.gz` | Linux      | 无损压缩 | 较小 | tar, 7-Zip         |
| `recitebot-linux.zip`    | Linux/通用 | ZIP      | 中等 | 任何 ZIP 工具      |
| `recitebot-windows.zip`  | Windows    | ZIP      | 中等 | Windows 资源管理器 |

---

## 🚀 快速开始

### 在 Linux 上使用

#### 方式 1：使用 tar.gz（推荐）

```bash
# 1. 下载文件（从 GitHub Release 页面下载）
# wget https://github.com/your-username/ReciteBot/releases/download/v1.0.0/recitebot-linux.tar.gz

# 2. 解压文件
tar -xzf recitebot-linux.tar.gz
cd build

# 3. 安装 Python 依赖
pip install -r ../../../requirements.txt

# 4. 安装 Node.js 依赖（可选，前端已预编译）
cd frontend
# npm install（不需要，已包含 dist/）
cd ..

# 5. 运行应用
python start_prod.py
```

#### 方式 2：使用 zip

```bash
# 1. 解压文件
unzip recitebot-linux.zip
cd build

# 2. 安装依赖
pip install flask==2.3.3 python-dotenv==1.2.1 openai==2.20.0

# 3. 运行应用
python start_prod.py
```

---

### 在 Windows 上使用

#### 步骤 1：解压文件

1. **下载** `recitebot-windows.zip` 从 GitHub Release 页面
2. **右键点击** zip 文件 → **解压到...** → 选择目标文件夹

   或使用命令行：

   ```powershell
   Expand-Archive -Path recitebot-windows.zip -DestinationPath .
   cd build
   ```

#### 步骤 2：安装 Python

1. 从 [python.org](https://www.python.org/downloads/) 下载 Python 3.12+
2. 安装时**勾选** "Add Python to PATH"
3. 验证安装：
   ```powershell
   python --version
   ```

#### 步骤 3：安装依赖

```powershell
# 使用 pip 安装必要的包
pip install flask==2.3.3 python-dotenv==1.2.1 openai==2.20.0
```

#### 步骤 4：运行应用

```powershell
# 进入项目目录
cd build

# 启动应用
python start_prod.py
```

应用会在以下地址运行：

- **后端 API**：http://localhost:9178
- **前端应用**：自动打开或访问前端地址

---

### 在 macOS 上使用

```bash
# 类似 Linux 步骤

# 1. 解压
tar -xzf recitebot-linux.tar.gz
cd build

# 2. 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install flask==2.3.3 python-dotenv==1.2.1 openai==2.20.0

# 4. 运行
python start_prod.py
```

---

## 📂 Release 文件结构

解压后的目录结构：

```
build/
├── backend/                    # Flask 后端代码
│   ├── app.py                 # 应用入口
│   ├── ai_call.py            # AI 处理脚本
│   └── routes/
│       ├── api.py            # API 端点
│       └── static.py         # 静态文件服务
├── frontend/                  # 前端应用
│   └── dist/                 # 预编译的前端文件✅
│       ├── index.html
│       ├── js/
│       ├── css/
│       └── assets/
├── user/                      # 用户数据目录
│   ├── list/
│   │   └── recite_list.json  # 背诵列表
│   └── *.json                # 用户书籍
├── start_prod.py             # 生产环境启动脚本
└── environment.yml           # Conda 环境配置
```

---

## 🔧 配置说明

### 修改应用配置

#### 1. 修改应用端口

编辑 `backend/app.py`，找到最后一行：

```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9178, debug=False)  # 修改 port 值
```

#### 2. 设置环境变量

在项目根目录创建 `.env` 文件：

```env
OPENAI_API_KEY=your_api_key_here
FLASK_ENV=production
DEBUG=False
```

#### 3. 配置 AI 服务

编辑 `backend/ai_call.py` 配置 OpenAI API：

```python
client = OpenAI(api_key="your-api-key")
```

---

## 🌐 访问应用

### 本地访问

应用启动后，访问：

- **Web UI**：http://localhost:5173（开发模式）
- **后端 API**：http://localhost:9178/api

### 远程访问

如果需要从其他机器访问：

```python
# 修改 backend/app.py
app.run(host='0.0.0.0', port=9178, debug=False)
```

然后从其他机器访问：

- `http://<your-ip>:9178/api`

---

## 📊 项目目录说明

| 目录              | 说明                     | 重要性  |
| ----------------- | ------------------------ | ------- |
| `backend/`        | Flask Web 框架、API 端点 | ✅ 核心 |
| `frontend/dist/`  | 已编译的 Vue.js 应用     | ✅ 核心 |
| `user/`           | 用户数据存储目录         | ⚠️ 重要 |
| `user/list/`      | 背诵列表存储             | ⚠️ 重要 |
| `environment.yml` | Conda 环境配置           | ℹ️ 参考 |

---

## ⚙️ 环境要求

| 组件          | 版本    | 必须 | 用途         |
| ------------- | ------- | ---- | ------------ |
| Python        | 3.12+   | ✅   | 后端运行环境 |
| Flask         | 2.3.3+  | ✅   | Web 框架     |
| python-dotenv | 1.2.1+  | ✅   | 环境变量管理 |
| openai        | 2.20.0+ | ✅   | AI 服务      |
| Node.js       | 18+     | ❌   | 仅开发时需要 |

---

## 🐛 故障排除

### 问题 1：Python 找不到 Flask

**症状**：`ModuleNotFoundError: No module named 'flask'`

**解决**：

```bash
pip install flask==2.3.3
```

### 问题 2：端口被占用

**症状**：`Address already in use`

**解决**（Linux/macOS）：

```bash
# 查找占用端口的进程
lsof -i :9178

# 终止进程（如果需要）
kill -9 <PID>
```

**解决**（Windows）：

```powershell
# 查找占用端口的进程
netstat -ano | findstr :9178

# 终止进程
taskkill /PID <PID> /F
```

### 问题 3：前端无法加载

**症状**：前端页面无法访问

**解决**：

1. 检查 `frontend/dist/` 目录是否存在
2. 检查后端是否正确提供静态文件
3. 检查浏览器控制台的错误信息

### 问题 4：AI 处理失败

**症状**：文本处理返回错误

**解决**：

1. 确保 `OpenAI API Key` 已正确配置
2. 检查 API 配额是否充足
3. 查看后端日志了解详细错误

---

## 📝 常用命令

### 启动应用

```bash
# 生产模式（推荐）
python start_prod.py

# 开发模式（带热更新）
python start_dev.py
```

### 检查日志

```bash
# 后端日志会输出到控制台
# 查看最近的错误信息
```

### 停止应用

```bash
# Linux/macOS
Ctrl + C

# Windows
Ctrl + C
```

---

## 🔒 安全建议

- ✅ 不要在公网上暴露 Python 调试模式
- ✅ 使用环境变量管理敏感信息（API Key）
- ✅ 定期备份 `user/` 目录中的数据
- ✅ 使用反向代理（如 nginx）在生产环境
- ✅ 启用 HTTPS 进行加密通信

---

## 📚 更多资源

- [Flask 官方文档](https://flask.palletsprojects.com/)
- [Vue.js 3 文档](https://vuejs.org/)
- [OpenAI API 文档](https://platform.openai.com/docs)
- [项目 GitHub 仓库](https://github.com/your-username/ReciteBot)

---

## 🆘 获取帮助

如遇到问题：

1. **查看日志**：运行时的控制台输出信息很有帮助
2. **检查环境**：确保 Python 和依赖包版本正确
3. **报告 Issue**：在 GitHub 仓库提交详细的问题描述
4. **查看 Wiki**：项目 Wiki 可能有已知问题的解决方案

---

**祝您使用愉快！** 🎉
