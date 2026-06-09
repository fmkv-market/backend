from enum import StrEnum


class QueueConfig(StrEnum):
    user_created = "user.created"
    item_added = "item.added"
    item_removed = "item.removed"