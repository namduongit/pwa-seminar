from pymongo.asynchronous.database import AsyncDatabase
from pymongo.results import InsertOneResult


class PoiOwnerRegistrationReposioty:
    def __init__(self, db: AsyncDatabase):
        self.collection = db["poi_owner_registration"]

    async def insert(self, document: dict) -> InsertOneResult:
        return await self.collection.insert_one(document)