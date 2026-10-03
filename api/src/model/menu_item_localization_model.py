from bson import ObjectId
from model._base import Base


class MenuItemLocalizationModel(Base):
    menu_item_id: ObjectId
    lang: str
    name: str
    description: str | None = None
    audio_url: str | None = None
