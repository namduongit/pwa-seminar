from model.admin_user_model import AdminUserModel
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.results import InsertOneResult


class AdminUserRepository:
    def __init__(self, db: AsyncDatabase):
        self.collection = db["admin_user"]

    async def find_pagination(self, search: dict):
        pass

    async def find_by_search(self, search: dict):
        document = await self.collection.find_one(search)
        if document is None:
            return None

        return AdminUserModel.model_validate(document)

    async def insert(self, document: dict) -> InsertOneResult:
        return await self.collection.insert_one(document)