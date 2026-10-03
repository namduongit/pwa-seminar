from datetime import datetime, timezone

from bson import ObjectId
from core.dependency import MongoDB
from fastapi import HTTPException, status
from model.poi_owner_registration_model import PoiOwnerRegistrationStatus
from repository.admin_user_repository import AdminUserRepository
from repository.poi_owner_registration_repository import PoiOwnerRegistrationReposioty
from schema.admin_schema import UpdatePoiPOwnerRegistration


class AdminService:
    def __init__(self, db: MongoDB):
        self.admin_user_repository = AdminUserRepository(db)
        self.poi_owner_registration_repository = PoiOwnerRegistrationReposioty(db)

    async def review_registration(
        self,
        id: str,
        body: UpdatePoiPOwnerRegistration,
    ) -> dict:
        registration_id = ObjectId(id)
        poi_owner_registration = await self.poi_owner_registration_repository.find_by_id(
            registration_id
        )

        if poi_owner_registration is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy đơn đăng ký",
            )

        if poi_owner_registration.status != PoiOwnerRegistrationStatus.PENDING.value:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Đơn đăng ký đã được xử lý",
            )

        admin_user = await self.admin_user_repository.find_one(
            {"_id": poi_owner_registration.user_id}
        )

        if admin_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy tài khoản của chủ quán",
            )

        is_approved = body.status == PoiOwnerRegistrationStatus.APPROVED
        user_updates: dict = {
            "is_poi_owner_verified": is_approved,
            "updated_at": datetime.now(timezone.utc),
        }

        await self.admin_user_repository.update_by_id(
            poi_owner_registration.user_id,
            user_updates,
        )

        await self.poi_owner_registration_repository.update_by_id(
            registration_id,
            {
                "status": body.status.value,
                "admin_note": body.admin_note or "",
                "updated_at": datetime.now(timezone.utc),
            },
        )
    
        return {
            "registration_id": id,
            "user_id": str(poi_owner_registration.user_id),
            "status": body.status.value,
            "admin_note": body.admin_note,
            "is_poi_owner_verified": is_approved,
        }
