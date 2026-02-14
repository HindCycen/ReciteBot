#!/usr/bin/env python3
"""
生产环境启动脚本
先构建前端，然后启动集成的Flask服务器（同时提供API和前端静态文件）
"""

import os
import sys
import subprocess
import signal


def build_frontend():
    """构建前端应用"""
    print("🏗️  构建前端应用...")
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    os.chdir(frontend_dir)

    # 检查是否安装了依赖
    if not os.path.exists('node_modules'):
        print("📦 安装前端依赖...")
        subprocess.run(['npm', 'install'], check=True)

    # 构建前端
    print("🔨 执行构建...")
    result = subprocess.run(['npm', 'run', 'build'], check=True)
    if result.returncode == 0:
        print("✅ 前端构建成功！")
    else:
        raise Exception("前端构建失败")

    # 返回项目根目录
    os.chdir(os.path.dirname(__file__))


def run_server():
    """启动集成的Flask服务器"""
    print("🚀 启动集成服务器...")
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)

    # 启动Flask服务器
    server_process = subprocess.Popen([sys.executable, 'app.py'],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      text=True)

    print("✅ 集成服务器已启动 (http://localhost:9178)")
    return server_process


def signal_handler(signum, frame):
    """处理中断信号"""
    print("\n🛑 正在停止服务器...")
    if 'server_process' in globals():
        server_process.terminate()
    print("👋 服务器已停止")
    sys.exit(0)


def main():
    """主函数"""
    print("🔧 ReciteBot 生产环境启动中...")
    print("=" * 50)

    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # 构建前端
        build_frontend()

        # 启动集成服务器
        global server_process
        server_process = run_server()

        print("=" * 50)
        print("🎉 生产环境已就绪！")
        print("🌐 访问 http://localhost:9178 开始使用")
        print("📝 按 Ctrl+C 停止服务")
        print("=" * 50)

        # 等待进程结束
        server_process.wait()

    except KeyboardInterrupt:
        signal_handler(None, None)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        signal_handler(None, None)


if __name__ == '__main__':
    main()
