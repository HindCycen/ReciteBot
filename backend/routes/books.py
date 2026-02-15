"""书籍管理相关的API端点"""

import os
import json
import glob
from datetime import datetime
from flask import request, jsonify
from .utils import USER_DIR, get_safe_filename


def save_book():
    """保存书籍的API端点"""
    try:
        # 获取请求数据
        data = request.get_json()
        if not data or "bookName" not in data or "chapters" not in data:
            return jsonify({"error": "缺少书籍名称或章节数据"}), 400

        book_name = data["bookName"].strip()
        chapters = data["chapters"]

        if not book_name:
            return jsonify({"error": "书籍名称不能为空"}), 400

        if not isinstance(chapters, list) or len(chapters) == 0:
            return jsonify({"error": "章节数据无效"}), 400

        # 验证章节数据格式
        for chapter in chapters:
            if (
                not isinstance(chapter, dict)
                or "Title" not in chapter
                or "Content" not in chapter
            ):
                return jsonify({"error": "章节数据格式错误"}), 400

        # 创建安全的文件名（移除非法字符）
        safe_book_name = get_safe_filename(book_name)

        file_path = os.path.join(USER_DIR, f"{safe_book_name}.json")

        # 保存JSON文件
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(chapters, f, ensure_ascii=False, indent=2)

        return jsonify(
            {"success": True, "message": f"书籍已保存为 {safe_book_name}.json"}
        )

    except Exception as e:
        print(f"保存书籍失败: {e}", file=__import__("sys").stderr)
        return jsonify({"error": "保存失败"}), 500


def get_books_list():
    """获取书籍列表的API端点"""
    try:
        # 查找所有.json文件
        json_files = glob.glob(os.path.join(USER_DIR, "*.json"))

        books = []
        for file_path in json_files:
            filename = os.path.basename(file_path)
            book_name = os.path.splitext(filename)[0]  # 移除.json扩展名

            # 获取文件修改时间
            mod_time = os.path.getmtime(file_path)
            mod_date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M")

            books.append(
                {"name": book_name, "filename": filename, "modified": mod_date}
            )

        # 按修改时间倒序排列
        books.sort(key=lambda x: x["modified"], reverse=True)

        return jsonify(books)

    except Exception as e:
        print(f"获取书籍列表失败: {e}", file=__import__("sys").stderr)
        return jsonify({"error": "获取书籍列表失败"}), 500


def get_book_content(filename):
    """获取指定书籍内容的API端点"""
    try:
        # 验证文件名安全性
        if not filename.endswith(".json"):
            return jsonify({"error": "无效的文件格式"}), 400

        # 防止路径遍历攻击
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(USER_DIR, safe_filename)

        # 检查文件是否存在
        if not os.path.exists(file_path):
            return jsonify({"error": "书籍不存在"}), 404

        # 读取文件内容
        with open(file_path, "r", encoding="utf-8") as f:
            content = json.load(f)

        return jsonify({"name": os.path.splitext(safe_filename)[0], "content": content})

    except json.JSONDecodeError:
        return jsonify({"error": "书籍文件格式错误"}), 500
    except Exception as e:
        print(f"读取书籍内容失败: {e}", file=__import__("sys").stderr)
        return jsonify({"error": "读取书籍内容失败"}), 500


def get_all_chapters():
    """获取所有书籍的所有章节（按书名分组）的API端点"""
    try:
        # 查找所有.json文件
        json_files = glob.glob(os.path.join(USER_DIR, "*.json"))

        books_with_chapters = []

        for file_path in sorted(json_files):
            filename = os.path.basename(file_path)
            book_name = os.path.splitext(filename)[0]

            try:
                # 读取书籍内容
                with open(file_path, "r", encoding="utf-8") as f:
                    chapters = json.load(f)

                # 验证章节数据格式
                if not isinstance(chapters, list):
                    continue

                # 过滤有效的章节（必须有Title和Content）
                valid_chapters = [
                    ch
                    for ch in chapters
                    if isinstance(ch, dict) and "Title" in ch and "Content" in ch
                ]

                if valid_chapters:
                    books_with_chapters.append(
                        {"book_name": book_name, "chapters": valid_chapters}
                    )
            except (json.JSONDecodeError, IOError):
                # 跳过无法读取的文件
                continue

        return jsonify(books_with_chapters)

    except Exception as e:
        print(f"获取所有章节失败: {e}", file=__import__("sys").stderr)
        return jsonify({"error": "获取所有章节失败"}), 500
