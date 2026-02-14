#!/usr/bin/env python3
"""
统一开发启动脚本
同时启动前端Vite开发服务器和后端Flask服务器
"""

import os
import sys
import subprocess
import signal
import time
from threading import Thread


def run_frontend():
    """启动前端Vite开发服务器"""
    print("🚀 启动前端开发服务器...")
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    os.chdir(frontend_dir)

    # 检查是否安装了依赖
    if not os.path.exists('node_modules'):
        print("📦 安装前端依赖...")
        subprocess.run(['npm', 'install'], check=True)

    # 启动Vite开发服务器
    frontend_process = subprocess.Popen(['npm', 'run', 'dev'],
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE,
                                        text=True)

    # 等待前端服务器启动
    time.sleep(2)
    print("✅ 前端开发服务器已启动 (http://localhost:5173)")

    return frontend_process


def run_backend():
    """启动后端Flask服务器"""
    print("🚀 启动后端服务器...")
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)

    # 启动Flask开发服务器
    backend_process = subprocess.Popen([sys.executable, 'app.py'],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       text=True)

    # 等待后端服务器启动
    time.sleep(2)
    print("✅ 后端服务器已启动 (http://localhost:9178)")

    return backend_process


def signal_handler(signum, frame):
    """处理中断信号"""
    print("\n🛑 正在停止所有服务...")
    if 'frontend_thread' in globals():
        frontend_process.terminate()
    if 'backend_thread' in globals():
        backend_process.terminate()
    print("👋 所有服务已停止")
    sys.exit(0)


def main():
    """主函数"""
    print("🔧 ReciteBot 开发环境启动中...")
    print("=" * 50)

    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # 启动前端
        global frontend_process
        frontend_process = run_frontend()

        # 返回项目根目录
        os.chdir(os.path.dirname(__file__))

        # 启动后端
        global backend_process
        backend_process = run_backend()

        print("=" * 50)
        print("🎉 开发环境已就绪！")
        print("🌐 访问 http://localhost:5173 开始使用")
        print("📝 按 Ctrl+C 停止所有服务")
        print("=" * 50)

        # 等待进程结束
        frontend_process.wait()
        backend_process.wait()

    except KeyboardInterrupt:
        signal_handler(None, None)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        signal_handler(None, None)


if __name__ == '__main__':
    main()
