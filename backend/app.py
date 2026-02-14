from flask import Flask, request, jsonify, send_from_directory
import subprocess
import sys
import os
import json

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)


@app.route('/api/process', methods=['POST'])
def process_text():
    try:
        # 获取请求数据
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': '缺少文本内容'}), 400

        input_text = data['text']
        if not input_text.strip():
            return jsonify({'error': '文本内容不能为空'}), 400

        # 调用ai_call.py脚本
        ai_script_path = os.path.join(os.path.dirname(__file__), 'ai_call.py')

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
            app.logger.error(f"AI脚本执行失败: {error_msg}")
            return jsonify({'error': f'处理失败: {error_msg}'}), 500

        # 解析AI返回的JSON结果
        try:
            ai_result = json.loads(result.stdout)
            return jsonify(ai_result)
        except json.JSONDecodeError as e:
            app.logger.error(f"JSON解析失败: {e}, 原始输出: {result.stdout}")
            return jsonify({'error': 'AI返回结果格式错误'}), 500

    except subprocess.TimeoutExpired:
        return jsonify({'error': '处理超时，请稍后重试'}), 500
    except Exception as e:
        app.logger.error(f"服务器内部错误: {e}")
        return jsonify({'error': '服务器内部错误'}), 500


@app.route('/')
def serve_index():
    """提供前端index.html页面"""
    return send_from_directory('../frontend', 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    """提供前端其他静态文件"""
    return send_from_directory('../frontend', filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9178, debug=True)
