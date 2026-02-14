import subprocess
import sys
import os
import json
from flask import request, jsonify

# 添加项目根目录到Python路径
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))))

# 确保user目录存在
user_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__)))), 'user')
os.makedirs(user_dir, exist_ok=True)


def process_text():
    """处理文本的API端点"""
    try:
        # 获取请求数据
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': '缺少文本内容'}), 400

        input_text = data['text']
        if not input_text.strip():
            return jsonify({'error': '文本内容不能为空'}), 400

        # 调用ai_call.py脚本
        ai_script_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'ai_call.py')

        # 使用subprocess调用Python脚本
        result = subprocess.run(
            [sys.executable, ai_script_path],
            input=input_text,
            text=True,
            capture_output=True,
            timeout=30  # 30秒超时
        )

        if result.returncode != 0:
            error_msg = result.stderr or "未知错误"
            # 这里无法直接使用app.logger，因为没有app上下文
            print(f"AI脚本执行失败: {error_msg}", file=sys.stderr)
            return jsonify({'error': f'处理失败: {error_msg}'}), 500

        # 解析AI返回的JSON结果
        try:
            ai_result = json.loads(result.stdout)
            return jsonify(ai_result)
        except json.JSONDecodeError as e:
            print(f"JSON解析失败: {e}, 原始输出: {result.stdout}", file=sys.stderr)
            return jsonify({'error': 'AI返回结果格式错误'}), 500

    except subprocess.TimeoutExpired:
        return jsonify({'error': '处理超时，请稍后重试'}), 500
    except Exception as e:
        print(f"服务器内部错误: {e}", file=sys.stderr)
        return jsonify({'error': '服务器内部错误'}), 500


def save_book():
    """保存书籍的API端点"""
    try:
        # 获取请求数据
        data = request.get_json()
        if not data or 'bookName' not in data or 'chapters' not in data:
            return jsonify({'error': '缺少书籍名称或章节数据'}), 400

        book_name = data['bookName'].strip()
        chapters = data['chapters']

        if not book_name:
            return jsonify({'error': '书籍名称不能为空'}), 400

        if not isinstance(chapters, list) or len(chapters) == 0:
            return jsonify({'error': '章节数据无效'}), 400

        # 验证章节数据格式
        for chapter in chapters:
            if not isinstance(
                    chapter, dict
            ) or 'Title' not in chapter or 'Content' not in chapter:
                return jsonify({'error': '章节数据格式错误'}), 400

        # 创建安全的文件名（移除非法字符）
        safe_book_name = "".join(
            c for c in book_name
            if c.isalnum() or c in (' ', '-', '_')).rstrip()
        if not safe_book_name:
            safe_book_name = "unnamed_book"

        file_path = os.path.join(user_dir, f"{safe_book_name}.json")

        # 保存JSON文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(chapters, f, ensure_ascii=False, indent=2)

        return jsonify({
            'success': True,
            'message': f'书籍已保存为 {safe_book_name}.json'
        })

    except Exception as e:
        print(f"保存书籍失败: {e}", file=sys.stderr)
        return jsonify({'error': '保存失败'}), 500
