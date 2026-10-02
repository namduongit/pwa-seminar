from model._base import Base


class RoleModel(Base):
    name: str
    permissions: list[str]
    is_system: bool
    priority: int