from enum import StrEnum


class QueueConfig(StrEnum):
    user_created_queue = "user.created"
    user_deleted_queue = "user.deleted"
