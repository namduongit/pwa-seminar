from enum import Enum

from bson import ObjectId
from model._base import Base


class PoiSubmissionStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class PoiSubmissionModel(Base):
    owner_id: ObjectId
    poi_id: ObjectId | None = None
    data: dict
    status: PoiSubmissionStatus = PoiSubmissionStatus.PENDING
    admin_note: str | None = None
