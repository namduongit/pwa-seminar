from enum import Enum

from bson import ObjectId
from model._base import Base
from pydantic import BaseModel


class AudioStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class GeoPointModel(BaseModel):
    type: str = "Point"
    coordinates: list[float]


class PoiModel(Base):
    owner_id: ObjectId | None = None
    category_id: ObjectId
    name: str
    description: str
    address: str
    location: GeoPointModel
    images: list[str]
    trigger_radius: float = 30
    is_active: bool = False
    activation_requested: bool = False
    audio_priority: int = 100
    audio_status: AudioStatus = AudioStatus.PENDING
