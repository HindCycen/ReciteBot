"""API路由主模块 - 汇总各功能模块的导出"""

# 导入AI处理相关函数
from .ai import process_text

# 导入书籍管理相关函数
from .books import save_book, get_books_list, get_book_content, get_all_chapters

# 导入背诵列表管理相关函数
from .recite import (
    get_recite_list,
    add_to_recite_list,
    remove_from_recite_list,
    mark_chapter_as_memorized,
    get_reciting_chapters,
    get_all_reciting_chapters,
)

# 导出所有API端点函数，供app.py导入
__all__ = [
    "process_text",
    "save_book",
    "get_books_list",
    "get_book_content",
    "get_all_chapters",
    "get_recite_list",
    "add_to_recite_list",
    "remove_from_recite_list",
    "mark_chapter_as_memorized",
    "get_reciting_chapters",
    "get_all_reciting_chapters",
]
