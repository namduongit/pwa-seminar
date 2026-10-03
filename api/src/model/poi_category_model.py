from model._base import Base


class PoiCategoryModel(Base):
    code: str
    name: str
    is_active: bool = True
