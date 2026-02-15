"""共享的工具函数和常量"""

import os
import sys

# 艾宾浩斯遗忘曲线复习间隔（天数）
EBBINGHAUS_INTERVALS = [1, 3, 7, 15, 30]

# 添加项目根目录到Python路径
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

# 确保user目录存在
USER_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "user"
)
os.makedirs(USER_DIR, exist_ok=True)


def get_safe_filename(name):
    """将文件名转换为安全的文件名（移除非法字符）"""
    safe_name = "".join(c for c in name if c.isalnum() or c in (" ", "-", "_")).rstrip()
    return safe_name if safe_name else "unnamed"


def get_recite_list_path():
    """获取背诵列表文件路径"""
    list_dir = os.path.join(USER_DIR, "list")
    os.makedirs(list_dir, exist_ok=True)
    return os.path.join(list_dir, "recite_list.json")
