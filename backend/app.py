import sys
import os
from flask import Flask

# 添加backend目录到Python路径，以便正确导入routes模块
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from routes.api import (
    process_text,
    save_book,
    get_books_list,
    get_book_content,
    get_all_chapters,
    get_recite_list,
    add_to_recite_list,
    remove_from_recite_list,
    get_reciting_chapters,
)
from routes.static import serve_index, serve_static


def create_app():
    """创建并配置Flask应用"""
    app = Flask(__name__)

    # 注册API路由
    app.add_url_rule("/api/process", view_func=process_text, methods=["POST"])
    app.add_url_rule("/api/save-book", view_func=save_book, methods=["POST"])
    app.add_url_rule("/api/books", view_func=get_books_list, methods=["GET"])
    app.add_url_rule("/api/all-chapters", view_func=get_all_chapters, methods=["GET"])
    app.add_url_rule(
        "/api/book/<filename>", view_func=get_book_content, methods=["GET"]
    )
    app.add_url_rule("/api/recite-list", view_func=get_recite_list, methods=["GET"])
    app.add_url_rule(
        "/api/recite-list/add", view_func=add_to_recite_list, methods=["POST"]
    )
    app.add_url_rule(
        "/api/recite-list/remove", view_func=remove_from_recite_list, methods=["POST"]
    )
    app.add_url_rule(
        "/api/reciting-chapters", view_func=get_reciting_chapters, methods=["GET"]
    )

    # 注册静态文件路由
    app.add_url_rule("/", view_func=serve_index, methods=["GET"])
    app.add_url_rule("/<path:filename>", view_func=serve_static, methods=["GET"])

    return app


# 创建应用实例
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9178, debug=True)
