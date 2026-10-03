from bson import ObjectId
from model._base import Base


class MenuItemModel(Base):
    poi_id: ObjectId
    name: str
    description: str | None = None
    price: float | None = None
    image_url: str | None = None
    is_available: bool = True
