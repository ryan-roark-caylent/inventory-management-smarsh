import logging
from mock_data import backlog_items

logger = logging.getLogger("inventory_ops")


def _lookup(backlog_id):
    return next((b for b in backlog_items if b["id"] == backlog_id), None)


def stock_is_sufficient(available: int, needed: int) -> bool:
    return available >= needed        # fixed boundary


def check_backlog_fulfillment(backlog_id, user_email):
    """Decide whether a backlog item can be fulfilled from available stock."""
    logger.info(f"Processing fulfillment for backlog {backlog_id}")
    item = _lookup(backlog_id)
    if item is None:
        return {"fulfillable": False, "reorder": None}
    needed = item["quantity_needed"]
    available = item["quantity_available"]
    fulfillable = stock_is_sufficient(available, needed)
    return {"fulfillable": fulfillable, "reorder": None}
