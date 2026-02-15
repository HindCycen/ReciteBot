"""艾宾浩斯遗忘曲线相关的逻辑

支持多种复习策略：
- aggressive: 激进策略，7天内掌握（用于短期学习）
- balanced: 均衡策略，14天掌握（用于常规学习）
- standard: 标准策略，30天掌握（经典艾宾浩斯）
"""

from datetime import datetime, timedelta
from .utils import EBBINGHAUS_INTERVALS, EBBINGHAUS_STRATEGIES, DEFAULT_STRATEGY


def get_strategy_intervals(strategy_name=None):
    """获取指定策略的复习间隔

    Args:
        strategy_name: 策略名称('aggressive', 'balanced', 'standard')
                      如果为None，使用默认策略

    Returns:
        复习间隔列表（单位：天）
    """
    if strategy_name is None:
        strategy_name = DEFAULT_STRATEGY

    if strategy_name not in EBBINGHAUS_STRATEGIES:
        strategy_name = DEFAULT_STRATEGY

    return EBBINGHAUS_STRATEGIES[strategy_name]["intervals"]


def get_strategy_info(strategy_name=None):
    """获取策略的详细信息

    Args:
        strategy_name: 策略名称

    Returns:
        包含策略信息的字典
    """
    if strategy_name is None:
        strategy_name = DEFAULT_STRATEGY

    if strategy_name not in EBBINGHAUS_STRATEGIES:
        strategy_name = DEFAULT_STRATEGY

    return EBBINGHAUS_STRATEGIES[strategy_name]


def calculate_next_review_time(review_count, strategy=None, base_time=None):
    """根据复习次数和策略计算下一次复习时间

    Args:
        review_count: 已复习的次数
        strategy: 复习策略名称('aggressive', 'balanced', 'standard')
                 如果为None，使用默认策略
        base_time: 基准时间，默认为当前时间

    Returns:
        下一次复习时间的ISO格式字符串
    """
    if base_time is None:
        base_time = datetime.now()
    elif isinstance(base_time, str):
        try:
            base_time = datetime.fromisoformat(base_time)
        except (ValueError, TypeError):
            base_time = datetime.now()

    intervals = get_strategy_intervals(strategy)

    if review_count < len(intervals):
        days = intervals[review_count]
    else:
        # 达到最后阶段后，保持最后的间隔
        days = intervals[-1]

    return (base_time + timedelta(days=days)).isoformat()


def calculate_review_cycle_days(strategy=None):
    """计算指定策略的完整学习周期天数

    Args:
        strategy: 复习策略名称

    Returns:
        完整学习周期需要的天数
    """
    strategy_info = get_strategy_info(strategy)
    return strategy_info["cycle_days"]


def get_completion_estimate(review_count, strategy=None):
    """获取学习完成度的估计

    Args:
        review_count: 已复习的次数
        strategy: 复习策略名称

    Returns:
        包含完成度信息的字典
    """
    intervals = get_strategy_intervals(strategy)
    completion_percentage = min((review_count / len(intervals)) * 100, 100)

    return {
        "current_review_count": review_count,
        "total_reviews_needed": len(intervals),
        "completion_percentage": round(completion_percentage, 1),
        "is_completed": review_count >= len(intervals),
        "next_review_count": review_count + 1,
    }


def is_time_to_review(next_review_at_str, current_time=None):
    """检查是否应该现在复习

    Args:
        next_review_at_str: 下次复习时间的ISO格式字符串
        current_time: 当前时间，默认为实际当前时间

    Returns:
        是否应该复习的布尔值
    """
    if not next_review_at_str:
        return True

    if current_time is None:
        current_time = datetime.now()
    elif isinstance(current_time, str):
        try:
            current_time = datetime.fromisoformat(current_time)
        except (ValueError, TypeError):
            current_time = datetime.now()

    try:
        next_review_at = datetime.fromisoformat(next_review_at_str)
        return next_review_at <= current_time
    except (ValueError, TypeError):
        return False


def get_time_until_next_review(next_review_at_str, current_time=None):
    """获取距离下次复习的时间差

    Args:
        next_review_at_str: 下次复习时间的ISO格式字符串
        current_time: 当前时间

    Returns:
        包含时间差信息的字典
    """
    if not next_review_at_str:
        return {"ready": True, "days": 0, "hours": 0, "message": "准备好复习"}

    if current_time is None:
        current_time = datetime.now()
    elif isinstance(current_time, str):
        try:
            current_time = datetime.fromisoformat(current_time)
        except (ValueError, TypeError):
            current_time = datetime.now()

    try:
        next_review_at = datetime.fromisoformat(next_review_at_str)
        time_diff = next_review_at - current_time

        if time_diff.total_seconds() <= 0:
            return {"ready": True, "days": 0, "hours": 0, "message": "现在可以复习"}

        days = time_diff.days
        hours = time_diff.seconds // 3600

        return {
            "ready": False,
            "days": days,
            "hours": hours,
            "message": f"还需等待 {days} 天 {hours} 小时",
        }
    except (ValueError, TypeError):
        return {"ready": False, "days": -1, "hours": -1, "message": "时间格式错误"}
