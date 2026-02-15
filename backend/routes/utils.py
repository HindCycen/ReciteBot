"""共享的工具函数和常量"""

import os
import sys

# 艾宾浩斯遗忘曲线复习间隔（天数）
# 标准间隔：适用于大多数学习场景
EBBINGHAUS_INTERVALS = [1, 3, 7, 15, 30]

# 艾宾浩斯复习策略配置（针对不同的背诵周期）
# 支持7天、14天、30天三种默认周期，每个周期有对应的复习频率
EBBINGHAUS_STRATEGIES = {
    "aggressive": {  # 激进策略（短周期学习，7天内掌握）
        "intervals": [0.5, 1, 2, 4],  # 天数
        "description": "短期集中学习，适合需要快速掌握的章节",
        "cycle_days": 7,
    },
    "balanced": {  # 均衡策略（标准周期学习，14天掌握）
        "intervals": [1, 3, 7, 14],  # 天数
        "description": "标准学习周期，适合日常学习",
        "cycle_days": 14,
    },
    "standard": {  # 标准策略（标准艾宾浩斯，30天掌握）
        "intervals": [1, 3, 7, 15, 30],  # 天数
        "description": "经典艾宾浩斯遗忘曲线，长期记忆效果最好",
        "cycle_days": 30,
    },
}

# 默认策略
DEFAULT_STRATEGY = "standard"

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
