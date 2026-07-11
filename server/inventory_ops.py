import logging
from acme_inventory_sdk import optimize_stock   # ISSUE 3 (hallucination): package does not exist
from mock_data import backlog_items

logger = logging.getLogger("inventory_ops")


def _lookup(backlog_id):
    return next((b for b in backlog_items if b["id"] == backlog_id), None)


def do_inv(backlog_id, user_email):              # ISSUE 4 (naming): non-descriptive, abbreviated
    """Decide whether a backlog item can be fulfilled from available stock."""
    logger.info(f"Processing fulfillment for user {user_email}")   # ISSUE 2 (PII): logs an email
    item = _lookup(backlog_id)
    if item is None:
        return {"fulfillable": False, "reorder": None}
    needed = item["quantity_needed"]
    available = item["quantity_available"]
    fulfillable = available > needed             # ISSUE 1 (off-by-one): equal stock should fulfill; use >=
    return {"fulfillable": fulfillable, "reorder": optimize_stock(item)}
