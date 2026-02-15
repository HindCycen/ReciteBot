"""背诵列表管理相关的API端点和工具函数"""

import os
import json
from datetime import datetime
from flask import request, jsonify
from .utils import USER_DIR, get_safe_filename, get_recite_list_path
from .ebbinghaus import (
    calculate_next_review_time,
    is_time_to_review,
    get_strategy_info,
    get_completion_estimate,
    get_time_until_next_review,
)


def load_recite_list():
    """加载背诵列表"""
    recite_path = get_recite_list_path()
    if not os.path.exists(recite_path):
        return []

    try:
        with open(recite_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_recite_list(recite_list):
    """保存背诵列表"""
    recite_path = get_recite_list_path()
    # 确保目录存在
    os.makedirs(os.path.dirname(recite_path), exist_ok=True)
    with open(recite_path, "w", encoding="utf-8") as f:
        json.dump(recite_list, f, ensure_ascii=False, indent=2)


def get_recite_list():
    """获取背诵列表的API端点"""
    try:
        recite_list = load_recite_list()
        return jsonify(recite_list)
    except Exception as e:
        print(f"获取背诵列表失败: {e}", file=__import__("sys").stderr)
        return jsonify({"error": "获取背诵列表失败"}), 500


def add_to_recite_list():
    """添加章节到背诵列表的API端点

    支持参数:
        - strategy: 复习策略 ('aggressive', 'balanced', 'standard')
                   默认为 'standard'
    """
    try:
        data = request.get_json()
        if not data or "book_name" not in data or "chapter_title" not in data:
            return jsonify({"error": "缺少书籍名称或章节标题"}), 400

        book_name = data["book_name"].strip()
        chapter_title = data["chapter_title"].strip()
        strategy = data.get("strategy", "standard")  # 获取复习策略，默认使用 'standard'

        if not book_name or not chapter_title:
            return jsonify({"error": "书籍名称和章节标题不能为空"}), 400

        # 加载现有的背诵列表
        recite_list = load_recite_list()

        # 创建唯一标识
        item_id = f"{book_name}:{chapter_title}"

        # 检查是否已经存在
        if not any(item.get("id") == item_id for item in recite_list):
            now = datetime.now().isoformat()
            recite_list.append(
                {
                    "id": item_id,
                    "book_name": book_name,
                    "chapter_title": chapter_title,
                    "strategy": strategy,  # 保存选择的复习策略
                    "added_at": now,
                    "review_count": 0,
                    "last_reviewed_at": None,
                    "next_review_at": now,
                }
            )
            save_recite_list(recite_list)

            # 返回策略信息
            strategy_info = get_strategy_info(strategy)
            return jsonify(
                {
                    "success": True,
                    "message": "已添加到背诵列表",
                    "strategy": strategy,
                    "strategy_description": strategy_info["description"],
                    "review_cycle_days": strategy_info["cycle_days"],
                }
            )

        return jsonify({"success": True, "message": "该章节已在背诵列表中"})

    except Exception as e:
        print(f"添加到背诵列表失败: {e}", file=__import__("sys").stderr)
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
        recite_list = load_recite_list()

        # 创建唯一标识
        item_id = f"{book_name}:{chapter_title}"

        # 移除该项
        recite_list = [item for item in recite_list if item.get("id") != item_id]
        save_recite_list(recite_list)

        return jsonify({"success": True, "message": "已从背诵列表移除"})

    except Exception as e:
        print(f"移除背诵列表项失败: {e}", file=__import__("sys").stderr)
        return jsonify({"error": "移除失败"}), 500


def mark_chapter_as_memorized():
    """标记章节为"背过了"，使用艾宾浩斯遗忘曲线计划下次复习时间"""
    try:
        data = request.get_json()
        if not data or "book_name" not in data or "chapter_title" not in data:
            return jsonify({"error": "缺少书籍名称或章节标题"}), 400

        book_name = data["book_name"].strip()
        chapter_title = data["chapter_title"].strip()

        if not book_name or not chapter_title:
            return jsonify({"error": "书籍名称和章节标题不能为空"}), 400

        # 加载现有的背诵列表
        recite_list = load_recite_list()

        # 创建唯一标识
        item_id = f"{book_name}:{chapter_title}"

        # 找到并更新该项
        for item in recite_list:
            if item.get("id") == item_id:
                # 增加复习次数
                item["review_count"] = item.get("review_count", 0) + 1
                # 更新最后复习时间
                item["last_reviewed_at"] = datetime.now().isoformat()
                # 获取该章节使用的复习策略
                strategy = item.get("strategy", "standard")
                # 根据艾宾浩斯曲线计算下次复习时间
                item["next_review_at"] = calculate_next_review_time(
                    item["review_count"], strategy=strategy
                )
                save_recite_list(recite_list)

                # 获取完成度信息
                completion = get_completion_estimate(
                    item["review_count"], strategy=strategy
                )
                time_until_review = get_time_until_next_review(item["next_review_at"])

                return jsonify(
                    {
                        "success": True,
                        "message": "已标记为背过，下次复习时间已更新",
                        "next_review_at": item["next_review_at"],
                        "review_count": item["review_count"],
                        "strategy": strategy,
                        "completion": completion,
                        "time_until_next_review": time_until_review,
                    }
                )

        return jsonify({"error": "章节不存在"}), 404

    except Exception as e:
        print(f"标记章节失败: {e}", file=__import__("sys").stderr)
        return jsonify({"error": "标记失败"}), 500


def get_reciting_chapters():
    """获取所有应该背诵的章节及其内容的API端点（根据艾宾浩斯遗忘曲线过滤）"""
    try:
        # 加载背诵列表
        recite_list = load_recite_list()

        # 按书籍名分组
        books_chapters = {}

        for item in recite_list:
            book_name = item.get("book_name")
            chapter_title = item.get("chapter_title")

            if not book_name or not chapter_title:
                continue

            # 检查是否应该现在复习（next_review_at <= 当前时间）
            if not is_time_to_review(item.get("next_review_at")):
                continue

            # 尝试从文件中读取章节内容
            safe_book_name = get_safe_filename(book_name)
            file_path = os.path.join(USER_DIR, f"{safe_book_name}.json")

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
                                "review_count": item.get("review_count", 0),
                                "last_reviewed_at": item.get("last_reviewed_at"),
                                "next_review_at": item.get("next_review_at"),
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
        print(f"获取背诵章节失败: {e}", file=__import__("sys").stderr)
        return jsonify({"error": "获取背诵章节失败"}), 500


def get_all_reciting_chapters():
    """获取所有正在背诵的章节（包括还未到复习时间的）"""
    try:
        # 加载背诵列表
        recite_list = load_recite_list()

        # 按书籍名分组
        books_chapters = {}

        for item in recite_list:
            book_name = item.get("book_name")
            chapter_title = item.get("chapter_title")

            if not book_name or not chapter_title:
                continue

            # 尝试从文件中读取章节内容
            safe_book_name = get_safe_filename(book_name)
            file_path = os.path.join(USER_DIR, f"{safe_book_name}.json")

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
                                "review_count": item.get("review_count", 0),
                                "last_reviewed_at": item.get("last_reviewed_at"),
                                "next_review_at": item.get("next_review_at"),
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
        print(f"获取所有背诵章节失败: {e}", file=__import__("sys").stderr)
        return jsonify({"error": "获取所有背诵章节失败"}), 500


def get_review_strategies():
    """获取所有可用的复习策略

    返回所有支持的复习策略及其详细信息
    """
    try:
        from .utils import EBBINGHAUS_STRATEGIES

        strategies = []
        for strategy_name, strategy_info in EBBINGHAUS_STRATEGIES.items():
            strategies.append(
                {
                    "name": strategy_name,
                    "description": strategy_info["description"],
                    "cycle_days": strategy_info["cycle_days"],
                    "intervals": strategy_info["intervals"],
                    "total_reviews": len(strategy_info["intervals"]),
                }
            )

        return jsonify(
            {
                "strategies": strategies,
                "default_strategy": "standard",
            }
        )
    except Exception as e:
        print(f"获取复习策略失败: {e}", file=__import__("sys").stderr)
        return jsonify({"error": "获取复习策略失败"}), 500


def change_recite_strategy():
    """修改背诵项目的复习策略并重新计算复习时间

    支持参数:
        - book_name: 书籍名称
        - chapter_title: 章节标题
        - strategy: 新的复习策略 ('aggressive', 'balanced', 'standard')
    """
    try:
        data = request.get_json()
        if (
            not data
            or "book_name" not in data
            or "chapter_title" not in data
            or "strategy" not in data
        ):
            return jsonify({"error": "缺少必要参数"}), 400

        book_name = data["book_name"].strip()
        chapter_title = data["chapter_title"].strip()
        new_strategy = data["strategy"].strip()

        if not book_name or not chapter_title or not new_strategy:
            return jsonify({"error": "参数不能为空"}), 400

        # 加载现有的背诵列表
        recite_list = load_recite_list()

        # 创建唯一标识
        item_id = f"{book_name}:{chapter_title}"

        # 找到并更新该项
        for item in recite_list:
            if item.get("id") == item_id:
                old_strategy = item.get("strategy", "standard")
                item["strategy"] = new_strategy

                # 保持当前的复习次数，但用新策略重新计算下次复习时间
                item["next_review_at"] = calculate_next_review_time(
                    item.get("review_count", 0), strategy=new_strategy
                )
                save_recite_list(recite_list)

                strategy_info = get_strategy_info(new_strategy)

                return jsonify(
                    {
                        "success": True,
                        "message": f"已将复习策略从 {old_strategy} 更改为 {new_strategy}",
                        "book_name": book_name,
                        "chapter_title": chapter_title,
                        "old_strategy": old_strategy,
                        "new_strategy": new_strategy,
                        "strategy_description": strategy_info["description"],
                        "next_review_at": item["next_review_at"],
                        "review_cycle_days": strategy_info["cycle_days"],
                    }
                )

        return jsonify({"error": "章节不存在"}), 404

    except Exception as e:
        print(f"修改复习策略失败: {e}", file=__import__("sys").stderr)
        return jsonify({"error": "修改复习策略失败"}), 500
