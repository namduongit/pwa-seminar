from bson import ObjectId
from model.role_model import RoleModel
from pymongo.asynchronous.database import AsyncDatabase


class RoleRepository:
    def __init__(self, db: AsyncDatabase):
        self.collection = db["role"]

    async def find_by_id(self, id: ObjectId) -> RoleModel | None:
        document = await self.collection.find_one({
            "_id": id
        })

        if document is None:
            return None

        return RoleModel.model_validate(document)

    async def find_by_name(self, name: str) -> RoleModel | None:
        document = await self.collection.find_one({"name": name})

        if document is None:
            return None

        return RoleModel.model_validate(document)
