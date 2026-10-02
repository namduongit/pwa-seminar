from bson import ObjectId
from model.poi_owner_registration_model import PoiOwnerRegistrationModel
from pymongo.asynchronous.database import AsyncDatabase
from pymongo.results import InsertOneResult


class PoiOwnerRegistrationReposioty:
    def __init__(self, db: AsyncDatabase):
        self.collection = db["poi_owner_registration"]
    
    async def find_by_user_id(self, user_id: ObjectId) -> PoiOwnerRegistrationModel | None:
        document = await self.collection.find_one({
            "user_id": user_id
        })

        if document is None:
            return None

        return PoiOwnerRegistrationModel.model_validate(document)

    async def insert_resource(self, document: dict) -> InsertOneResult:
        return await self.collection.insert_one(document)