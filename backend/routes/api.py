import subprocess
import sys
import os
import json
import glob
from flask import request, jsonify

# 添加项目根目录到Python路径
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# 确保user目录存在
user_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "user"
)
os.makedirs(user_dir, exist_ok=True)


def process_text():
    """处理文本的API端点"""
    try:
        # 获取请求数据
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "缺少文本内容"}), 400

        input_text = data["text"]
        if not input_text.strip():
            return jsonify({"error": "文本内容不能为空"}), 400

        # 调用ai_call.py脚本
        ai_script_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ai_call.py"
        )

        # 使用subprocess调用Python脚本
        result = subprocess.run(
            [sys.executable, ai_script_path],
            input=input_text,
            text=True,
            capture_output=True,
            timeout=30,  # 30秒超时
        )

        if result.returncode != 0:
            error_msg = result.stderr or "未知错误"
            # 这里无法直接使用app.logger，因为没有app上下文
            print(f"AI脚本执行失败: {error_msg}", file=sys.stderr)
            return jsonify({"error": f"处理失败: {error_msg}"}), 500

        # 解析AI返回的JSON结果
        try:
            ai_result = json.loads(result.stdout)
            return jsonify(ai_result)
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}, 原始输出: {result.stdout}", file=sys.stderr)
            return jsonify({"error": "AI返回结果格式错误"}), 500

    except subprocess.TimeoutExpired:
        return jsonify({"error": "处理超时，请稍后重试"}), 500
    except Exception as e:
        print(f"服务器内部错误: {e}", file=sys.stderr)
        return jsonify({"error": "服务器内部错误"}), 500


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
        safe_book_name = "".join(
            c for c in book_name if c.isalnum() or c in (" ", "-", "_")
        ).rstrip()
        if not safe_book_name:
            safe_book_name = "unnamed_book"

        file_path = os.path.join(user_dir, f"{safe_book_name}.json")

        # 保存JSON文件
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(chapters, f, ensure_ascii=False, indent=2)

        return jsonify(
            {"success": True, "message": f"书籍已保存为 {safe_book_name}.json"}
        )

    except Exception as e:
        print(f"保存书籍失败: {e}", file=sys.stderr)
        return jsonify({"error": "保存失败"}), 500


def get_books_list():
    """获取书籍列表的API端点"""
    try:
        # 查找所有.json文件
        json_files = glob.glob(os.path.join(user_dir, "*.json"))

        books = []
        for file_path in json_files:
            filename = os.path.basename(file_path)
            book_name = os.path.splitext(filename)[0]  # 移除.json扩展名

            # 获取文件修改时间
            mod_time = os.path.getmtime(file_path)
            from datetime import datetime

            mod_date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d %H:%M")

            books.append(
                {"name": book_name, "filename": filename, "modified": mod_date}
            )

        # 按修改时间倒序排列
        books.sort(key=lambda x: x["modified"], reverse=True)

        return jsonify(books)

    except Exception as e:
        print(f"获取书籍列表失败: {e}", file=sys.stderr)
        return jsonify({"error": "获取书籍列表失败"}), 500


def get_book_content(filename):
    """获取指定书籍内容的API端点"""
    try:
        # 验证文件名安全性
        if not filename.endswith(".json"):
            return jsonify({"error": "无效的文件格式"}), 400

        # 防止路径遍历攻击
        safe_filename = os.path.basename(filename)
        file_path = os.path.join(user_dir, safe_filename)

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
        print(f"读取书籍内容失败: {e}", file=sys.stderr)
        return jsonify({"error": "读取书籍内容失败"}), 500


def get_all_chapters():
    """获取所有书籍的所有章节（按书名分组）的API端点"""
    try:
        # 查找所有.json文件
        json_files = glob.glob(os.path.join(user_dir, "*.json"))

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
        print(f"获取所有章节失败: {e}", file=sys.stderr)
        return jsonify({"error": "获取所有章节失败"}), 500


def _get_recite_list_path():
    """获取背诵列表文件路径"""
    list_dir = os.path.join(user_dir, "list")
    os.makedirs(list_dir, exist_ok=True)
    return os.path.join(list_dir, "recite_list.json")


def _load_recite_list():
    """加载背诵列表"""
    recite_path = _get_recite_list_path()
    if not os.path.exists(recite_path):
        return []

    try:
        with open(recite_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _save_recite_list(recite_list):
    """保存背诵列表"""
    recite_path = _get_recite_list_path()
    # 确保目录存在
    os.makedirs(os.path.dirname(recite_path), exist_ok=True)
    with open(recite_path, "w", encoding="utf-8") as f:
        json.dump(recite_list, f, ensure_ascii=False, indent=2)


def get_recite_list():
    """获取背诵列表的API端点"""
    try:
        recite_list = _load_recite_list()
        return jsonify(recite_list)
    except Exception as e:
        print(f"获取背诵列表失败: {e}", file=sys.stderr)
        return jsonify({"error": "获取背诵列表失败"}), 500


def add_to_recite_list():
    """添加章节到背诵列表的API端点"""
    try:
        data = request.get_json()
        if not data or "book_name" not in data or "chapter_title" not in data:
            return jsonify({"error": "缺少书籍名称或章节标题"}), 400

        book_name = data["book_name"].strip()
        chapter_title = data["chapter_title"].strip()

        if not book_name or not chapter_title:
            return jsonify({"error": "书籍名称和章节标题不能为空"}), 400

        # 加载现有的背诵列表
        recite_list = _load_recite_list()

        # 创建唯一标识
        item_id = f"{book_name}:{chapter_title}"

        # 检查是否已经存在
        if not any(item.get("id") == item_id for item in recite_list):
            recite_list.append(
                {
                    "id": item_id,
                    "book_name": book_name,
                    "chapter_title": chapter_title,
                    "added_at": __import__("datetime").datetime.now().isoformat(),
                }
            )
            _save_recite_list(recite_list)

        return jsonify({"success": True, "message": "已添加到背诵列表"})

    except Exception as e:
        print(f"添加到背诵列表失败: {e}", file=sys.stderr)
        return jsonify({"error": "添加失败"}), 500


def remove_from_recite_list():
    """从背诵列表移除章节的API端点"""
    try:
        data = request.get_json()
        if not data or "book_name" not in data or "chapter_title" not in data:
            return jsonify({"error": "缺少书籍名称或章节标题"}), 400

        book_name = data["book_name"].strip()
        chapter_title = data["chapter_title"].strip()

        if not book_name or not chapter_title:
            return jsonify({"error": "书籍名称和章节标题不能为空"}), 400

        # 加载现有的背诵列表
        recite_list = _load_recite_list()

        # 创建唯一标识
        item_id = f"{book_name}:{chapter_title}"

        # 移除该项
        recite_list = [item for item in recite_list if item.get("id") != item_id]
        _save_recite_list(recite_list)

        return jsonify({"success": True, "message": "已从背诵列表移除"})

    except Exception as e:
        print(f"移除背诵列表项失败: {e}", file=sys.stderr)
        return jsonify({"error": "移除失败"}), 500


def get_reciting_chapters():
    """获取所有背诵中的章节及其内容的API端点"""
    try:
        # 加载背诵列表
        recite_list = _load_recite_list()

        # 按书籍名分组
        books_chapters = {}

        for item in recite_list:
            book_name = item.get("book_name")
            chapter_title = item.get("chapter_title")

            if not book_name or not chapter_title:
                continue

            # 尝试从文件中读取章节内容
            safe_book_name = "".join(
                c for c in book_name if c.isalnum() or c in (" ", "-", "_")
            ).rstrip()
            if not safe_book_name:
                safe_book_name = "unnamed_book"

            file_path = os.path.join(user_dir, f"{safe_book_name}.json")

            try:
                if not os.path.exists(file_path):
                    continue

                with open(file_path, "r", encoding="utf-8") as f:
                    chapters = json.load(f)

                # 查找匹配的章节
                for chapter in chapters:
                    if (
                        isinstance(chapter, dict)
                        and chapter.get("Title") == chapter_title
                    ):
                        if book_name not in books_chapters:
                            books_chapters[book_name] = []

                        books_chapters[book_name].append(
                            {
                                "Title": chapter.get("Title"),
                                "Content": chapter.get("Content"),
                                "added_at": item.get("added_at"),
                            }
                        )
                        break
            except (json.JSONDecodeError, IOError):
                continue

        # 转换为列表格式
        result = []
        for book_name, chapters in books_chapters.items():
            result.append(
                {
                    "book_name": book_name,
                    "chapters": chapters,
                }
            )

        return jsonify(result)

    except Exception as e:
        print(f"获取背诵章节失败: {e}", file=sys.stderr)
        return jsonify({"error": "获取背诵章节失败"}), 500
