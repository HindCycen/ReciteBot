import os
from flask import send_from_directory, send_file


def serve_index():
    """提供前端index.html页面"""
    frontend_dist = os.path.join(
        os.path.dirname(__file__), "..", "..", "frontend", "dist"
    )
    if os.path.exists(frontend_dist):
        # 生产环境：提供构建后的文件
        return send_from_directory(frontend_dist, "index.html")
    else:
        # 开发环境：提供源码中的index.html
        return send_from_directory("../frontend", "index.html")


def serve_static(filename):
    """提供前端其他静态文件"""
    frontend_dist = os.path.join(
        os.path.dirname(__file__), "..", "..", "frontend", "dist"
    )
    if os.path.exists(frontend_dist):
        # 生产环境：提供构建后的文件
        file_path = os.path.join(frontend_dist, filename)
        if os.path.exists(file_path):
            return send_from_directory(frontend_dist, filename)
        else:
            # 如果文件不存在，返回index.html（用于Vue Router的history模式）
            return send_from_directory(frontend_dist, "index.html")
    else:
        # 开发环境：提供源码中的文件
        return send_from_directory("../frontend", filename)
