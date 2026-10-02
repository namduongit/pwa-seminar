from bson import ObjectId
from core.dependency import MongoDB
from fastapi import HTTPException, status
from model.poi_owner_registration_model import PoiOwnerRegistrationModel
from repository.poi_owner_registration_repository import PoiOwnerRegistrationReposioty


class OwnerService:
    def __init__(self, db: MongoDB):
        self.poi_owner_registration_repository = PoiOwnerRegistrationReposioty(db)

    async def get_registration_status(self, user_id: str) -> PoiOwnerRegistrationModel:
        if not ObjectId.is_valid(user_id):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Phiên đăng nhập không hợp lệ",
            )

        poi_owner_registration = await self.poi_owner_registration_repository.find_by_user_id(
            ObjectId(user_id)
        )

        if poi_owner_registration is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tài khoản chưa đăng ký doanh nghiệp"
            )

        return poi_owner_registration 
