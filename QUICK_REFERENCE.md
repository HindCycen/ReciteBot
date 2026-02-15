# 快速参考指南

## 📦 Release 文件使用

### Linux 用户

```bash
# 下载后解压
tar -xzf recitebot-linux.tar.gz
cd build

# 安装依赖
pip install -r ../requirements.txt

# 运行
python start_prod.py
```

### Windows 用户

```powershell
# 解压
Expand-Archive -Path recitebot-windows.zip -DestinationPath .
cd build

# 安装依赖
pip install flask==2.3.3 python-dotenv==1.2.1 openai==2.20.0

# 运行
python start_prod.py
```

---

## 🚀 发布新版本

### 步骤 1-3：创建和推送标签

```bash
git tag v1.0.0
git push origin v1.0.0
```

### 步骤 4：等待自动构建

- 打开 GitHub Actions 标签页
- 查看 Build and Release 工作流

### 步骤 5：从 Releases 下载

- 进入 Releases 页面
- 下载所需平台的文件

---

## 🔧 常用命令

### Git Tag 操作

```bash
git tag -l                           # 列显所有标签
git tag v1.0.0                       # 创建轻量级标签
git tag -a v1.0.0 -m "message"      # 创建附注标签
git push origin v1.0.0              # 推送单个标签
git push origin --tags              # 推送所有标签
git tag -d v1.0.0                   # 删除本地标签
git push origin :refs/tags/v1.0.0   # 删除远程标签
```

### 监控构建

```bash
# 在线查看日志
# GitHub → Actions → Build and Release → Click job

# 查看构建状态
curl -s https://api.github.com/repos/USERNAME/ReciteBot/actions/runs | jq '.workflow_runs[0]'
```

---

## 📁 Release 文件结构

```
build/
├── frontend/dist/    # 前端已编译 ✅
├── backend/         # Flask 应用
├── user/            # 用户数据
└── start_prod.py    # 启动脚本
```

---

## ⚡ 快速启动（3 步）

### 1️⃣ 解压

```bash
tar -xzf recitebot-linux.tar.gz && cd build
```

### 2️⃣ 安装

```bash
pip install -r ../requirements.txt 2>/dev/null || pip install flask==2.3.3 python-dotenv==1.2.1 openai==2.20.0
```

### 3️⃣ 运行

```bash
python start_prod.py
```

**应用已启动！** 访问 http://localhost:9178

---

## 🔗 重要链接

| 资源             | 链接                        |
| ---------------- | --------------------------- |
| Releases         | `/releases`                 |
| Actions          | `/actions`                  |
| Issues           | `/issues`                   |
| GitHub 文档      | https://docs.github.com     |
| 项目使用指南     | `./RELEASE_USAGE_GUIDE.md`  |
| Actions 配置指南 | `./GITHUB_ACTIONS_SETUP.md` |

---

## ❓ 常见问题速解

| 问题                         | 解决方案                           |
| ---------------------------- | ---------------------------------- |
| `ModuleNotFoundError: flask` | `pip install flask==2.3.3`         |
| 端口被占用                   | 修改 `app.run(port=9179)`          |
| 前端无法加载                 | 检查 `frontend/dist/` 是否存在     |
| AI 处理失败                  | 检查 API Key 是否配置              |
| Windows 构建失败             | 查看工作流日志中的 PowerShell 错误 |

---

## 📋 发布检查清单

- [ ] 代码已提交 `git add . && git commit -m "msg"`
- [ ] 版本标签正确 `git tag v1.0.0`
- [ ] 标签已推送 `git push origin v1.0.0`
- [ ] Actions 工作流运行中
- [ ] 所有 jobs 已完成 ✅
- [ ] Release 已生成
- [ ] 文件已上传到 Release
- [ ] 下载并测试文件
- [ ] 宣布新版本

---

## 🎯 版本号规则

```
v MAJOR . MINOR . PATCH

v1.0.0  → 首发版本
v1.1.0  → 新功能
v1.1.1  → Bug 修复
v2.0.0  → 大版本
```

---

## 💡 Pro 技巧

### 一条命令发布

```bash
git add . && git commit -m "Release v1.0.0" && git tag v1.0.0 && git push origin main v1.0.0
```

### 检查 Actions 状态

```bash
# 最近 5 个工作流运行
curl -s https://api.github.com/repos/USERNAME/repo/actions/runs?per_page=5 | jq '.workflow_runs[] | {name, conclusion, status}'
```

### 从 Release 直接下载

```bash
# Linux
wget https://github.com/USERNAME/ReciteBot/releases/download/v1.0.0/recitebot-linux.tar.gz

# macOS
curl -L https://github.com/USERNAME/ReciteBot/releases/download/v1.0.0/recitebot-linux.tar.gz -o recitebot-linux.tar.gz
```

---

Last updated: 2026-02-15
