from datetime import datetime

from bson import ObjectId
from model._base import Base


class AuditLogModel(Base):
    user_id: ObjectId | None = None
    action: str | None = None
    resource: str | None = None
    timestamp: datetime | None = None
