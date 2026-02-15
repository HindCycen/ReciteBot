# GitHub Actions CI/CD 配置指南

## 📋 工作流说明

本项目配置了完整的 GitHub Actions CI/CD 流程，支持 **Linux** 和 **Windows** 多平台构建。

---

## 🔄 工作流详解

### 1. Build and Release (`.github/workflows/build-and-release.yml`)

自动构建和打包项目，支持多个平台。

#### 工作流组成

**Job 1: build-linux**

- 在 Ubuntu 上构建
- 生成 `recitebot-linux.tar.gz` 和 `recitebot-linux.zip`
- 打包前端已编译文件和后端代码

**Job 2: build-windows**

- 在 Windows 上构建
- 生成 `recitebot-windows.zip`
- 使用 PowerShell 脚本处理 Windows 特殊路径

**Job 3: create-release**

- 下载所有平台的构建文件
- 创建 GitHub Release
- 上传所有文件到 Release

#### 触发方式

**方式 1：Git Tag（推荐 - 自动发布）**

```bash
git tag v1.0.0
git push origin v1.0.0
```

**方式 2：手动触发（Workflow Dispatch）**

1. GitHub 仓库 → Actions 标签
2. Build and Release → Run workflow
3. 可选输入版本号

**方式 3：Workflow 文件更新（自动）**
编辑 `.github/workflows/build-and-release.yml` 并 push 时自动运行

---

### 2. CI Build Check (`.github/workflows/build-check.yml`)

持续集成检查，确保每次推送都能正确构建。

#### Linux 检查 (build-check-linux)

运行平台：Ubuntu

- Python 语法检查
- Node.js 依赖安装
- 前端编译验证
- 构建输出验证

#### Windows 检查 (build-check-windows)

运行平台：Windows

- Python 语法检查（PowerShell）
- Node.js 依赖安装
- 前端编译验证
- 构建输出验证
- 项目结构检查

#### 触发条件

```yaml
push:
  branches: [main, develop, master]

pull_request:
  branches: [main, develop, master]
```

---

## 📦 构建输出详解

### Linux 构建文件

| 文件                     | 格式     | 用途       | 大小 |
| ------------------------ | -------- | ---------- | ---- |
| `recitebot-linux.tar.gz` | 无损压缩 | Linux/Unix | 较小 |
| `recitebot-linux.zip`    | ZIP      | 通用       | 中等 |

### Windows 构建文件

| 文件                    | 格式 | 用途    | 大小 |
| ----------------------- | ---- | ------- | ---- |
| `recitebot-windows.zip` | ZIP  | Windows | 中等 |

---

## 🚀 发布流程详解

### 完整流程

```
1. 本地提交代码
         ↓
2. 创建 Git tag (v1.0.0)
         ↓
3. git push origin v1.0.0
         ↓
4. GitHub Actions 触发
         ↓
   ┌─────────────────┬──────────────────┐
   ↓                 ↓                  ↓
Linux 构建      Windows 构建      等待完成
   ↓                 ↓
生成 2 个文件   生成 1 个文件
   ↓                 ↓
   └────────────┬────────────┘
                ↓
           create-release job
                ↓
           下载所有文件
                ↓
           创建 Release
                ↓
           上传到 GitHub 🎉
```

### 具体步骤

#### 第一步：本地开发完成

```bash
git add .
git commit -m "Feature: add new functionality"
```

#### 第二步：创建版本标签

```bash
# 推荐使用语义化版本
git tag -a v1.0.0 -m "Release 1.0.0"

# 查看标签
git tag -l
```

#### 第三步：推送标签

```bash
git push origin v1.0.0
# 或推送所有标签
git push origin --tags
```

#### 第四步：监控构建

1. 打开 GitHub 仓库
2. 点击 **Actions** 标签
3. 查看 **Build and Release** 工作流
4. 等待所有 job 完成（通常 5-15 分钟）

#### 第五步：验证发布

1. 进入 **Releases** 页面
2. 查看新版本
3. 下载构建文件

---

## 🔍 监控和调试

### 查看工作流日志

1. **GitHub 界面**
   - Actions 标签 → 工作流 → 具体运行 → 点击 job 查看详细日志

2. **日志内容说明**
   ```
   ✅ 绿色 ✓ - 步骤成功
   ❌ 红色 ✗ - 步骤失败
   ⚠️  黄色 ⊘ - 步骤警告
   ⏳ 灰色 → - 步骤进行中
   ```

### 常见问题排查

**问题 1：前端构建失败**

- 检查 Node.js 版本兼容性
- 查看 npm install 日志
- 验证 package.json 配置

**问题 2：Python 语法错误**

- 查看具体错误行号
- 验证 Python 版本（3.12）
- 检查依赖包版本

**问题 3：Release 创建失败**

- 检查 GitHub Token 权限
- 确保标签格式正确（v\*）
- 查看 create-release job 日志

---

## 🔧 自定义配置

### 修改 Python 版本

编辑工作流文件，找到：

```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: "3.12" # 改为需要的版本
```

### 修改 Node.js 版本

```yaml
- name: Set up Node.js
  uses: actions/setup-node@v4
  with:
    node-version: "18.x" # 改为需要的版本
```

### 添加自定义构建步骤

在 build-linux 或 build-windows job 中添加：

```yaml
- name: Your custom step
  shell: bash # 或 powershell（Windows）
  run: |
    echo "Execute custom command"
    # 你的命令
```

### 修改压缩格式

在 build-windows job 中修改压缩逻辑：

```powershell
# 修改输出文件名
$DestinationPath = "recitebot-windows-custom.zip"
```

---

## 📊 工作流性能优化

### 缓存依赖

添加缓存以加快构建速度：

```yaml
- name: Cache npm packages
  uses: actions/cache@v3
  with:
    path: frontend/node_modules
    key: ${{ runner.os }}-npm-${{ hashFiles('**/package-lock.json') }}
```

### 并行构建

当前工作流已配置 Linux 和 Windows 并行构建：

```yaml
build-windows:
  needs: [] # 不依赖其他 job，并行运行
```

### 减少工件大小

在 create-release job 中清理不必要文件：

```bash
rm -rf build/__pycache__  # 删除编译缓存
rm -rf build/node_modules  # 删除 node_modules
```

---

## 🎯 最佳实践

### 版本命名规范

使用语义化版本（Semantic Versioning）：

```
v<MAJOR>.<MINOR>.<PATCH>[-PRERELEASE]

示例：
v1.0.0        - 首个发布版本
v1.1.0        - 新增功能
v1.1.1        - Bug 修复
v2.0.0        - 主版本更新（不兼容）
v1.0.0-beta   - Beta 版
v1.0.0-rc.1   - Release Candidate
```

### 提交信息最佳实践

```bash
git tag -a v1.0.0 -m "Release v1.0.0

Features:
- Add recite list functionality
- Support Windows builds

Bug Fixes:
- Fix API response format
- Improve error handling

Breaking Changes:
- None
"
```

### 发布清单

发布前检查：

- ✅ 所有测试通过
- ✅ 文档已更新
- ✅ 版本号已更新
- ✅ CHANGELOG 已更新
- ✅ 标签创建正确
- ✅ 提交消息清晰

---

## 🔐 安全配置

### GitHub Token 权限

工作流使用的 `GITHUB_TOKEN` 会自动获得：

- ✅ `contents: write` - 创建 Release 和上传文件
- ✅ `pull-requests: read` - 读取 PR 信息

### 环保变量

避免在工作流中硬编码敏感信息：

```yaml
# ❌ 不要这样做
- run: export API_KEY=sk-xxx

# ✅ 应该这样做
- run: echo "API_KEY=${{ secrets.OPENAI_API_KEY }}"
```

---

## 📝 故障恢复

### 重新运行失败的工作流

1. GitHub Actions 页面 → 失败的工作流
2. **Re-run failed jobs** 或 **Re-run all jobs**

### 删除失败的 Release

```bash
# 删除本地标签
git tag -d v1.0.0

# 删除远程标签
git push origin :refs/tags/v1.0.0

# 或使用
git push origin --delete v1.0.0

# 然后重新创建
git tag v1.0.0
git push origin v1.0.0
```

---

## 📚 相关资源

- [GitHub Actions 官方文档](https://docs.github.com/en/actions)
- [GitHub 发布说明](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [软件版本控制最佳实践](https://semver.org/lang/zh-CN/)
- [项目 Release 使用指南](./RELEASE_USAGE_GUIDE.md)

---

## 🆘 获取帮助

问题排查步骤：

1. **查看工作流日志** - 查找错误信息
2. **检查依赖版本** - 确保版本兼容
3. **验证文件结构** - 检查必要文件是否存在
4. **查看 GitHub Issues** - 搜索已知问题
5. **提交新 Issue** - 详细描述问题和日志

---

**祝您的 CI/CD 流程运行顺畅！** 🚀
