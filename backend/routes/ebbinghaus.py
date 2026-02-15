"""艾宾浩斯遗忘曲线相关的逻辑"""

from datetime import datetime, timedelta
from .utils import EBBINGHAUS_INTERVALS


def calculate_next_review_time(review_count):
    """根据复习次数计算下一次复习时间"""
    if review_count < len(EBBINGHAUS_INTERVALS):
        days = EBBINGHAUS_INTERVALS[review_count]
    else:
        days = EBBINGHAUS_INTERVALS[-1]  # 最后间隔固定为30天

    return (datetime.now() + timedelta(days=days)).isoformat()


def is_time_to_review(next_review_at_str):
    """检查是否应该现在复习"""
    if not next_review_at_str:
        return True

    try:
        next_review_at = datetime.fromisoformat(next_review_at_str)
        return next_review_at <= datetime.now()
    except (ValueError, TypeError):
        return False
