from bson import ObjectId
from model._base import Base


class OwnerNotificationModel(Base):
    owner_id: ObjectId
    submission_id: ObjectId
    admin_note: str | None = None
    is_read: bool = False
