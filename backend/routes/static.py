import os
from flask import send_from_directory


def serve_index():
    """提供前端index.html页面"""
    return send_from_directory('../frontend', 'index.html')


def serve_static(filename):
    """提供前端其他静态文件"""
    return send_from_directory('../frontend', filename)
