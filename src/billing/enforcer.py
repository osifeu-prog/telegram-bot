from src.billing.plans import PLANS
from src.billing.meter import get_usage


def check_limit(user_id: int, plan_name: str, key: str) -> bool:
    plan = PLANS.get(plan_name)

    if not plan:
        return False

    usage = get_usage(user_id).get(key, 0)

    limit = getattr(plan, f"{key}_limit", None)

    if limit is None:
        return True

    return usage < limit
