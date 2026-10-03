from bson import ObjectId
from model._base import Base


class PoiLocalizationModel(Base):
    poi_id: ObjectId
    lang: str
    category: str
    name: str
    description: str
    audio_url: str | None = None
