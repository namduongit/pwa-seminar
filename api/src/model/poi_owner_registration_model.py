from enum import Enum

from bson import ObjectId
from model._base import Base


class PoiOwnerRegistrationStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class PoiOwnerRegistrationModel(Base):
    user_id: ObjectId   
    business_name: str
    business_address: str
    admin_note: str
    status: PoiOwnerRegistrationStatus