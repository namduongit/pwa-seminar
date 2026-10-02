from datetime import datetime, timezone

from core.dependency import MongoDB
from core.security import (
    compare_password,
    encrypt_pii,
    generate_access_token,
    generate_refresh_token,
    hash_password,
)
from fastapi import HTTPException, status
from model.admin_user_model import AdminUserModel
from model.poi_owner_registration_model import (
    PoiOwnerRegistrationModel,
    PoiOwnerRegistrationStatus,
)
from repository.admin_user_repository import AdminUserRepository
from repository.poi_owner_registration_repository import PoiOwnerRegistrationReposioty
from repository.role_repository import RoleRepository
from schema.auth_schema import Login, RegisterPoiOwner


class AuthService:
    def __init__(self, db: MongoDB):
        self.admin_user_repository = AdminUserRepository(db)
        self.poi_owner_registration_repository = PoiOwnerRegistrationReposioty(db)
        self.role_repository = RoleRepository(db)

    async def register_poi_owner(self, body: RegisterPoiOwner):
        # Check email, phone
        existing = await self.admin_user_repository.find_by_search(
            {"$or": [{"email": body.email}, {"phone": body.phone}]}
        )

        if existing is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email hoặc SĐT đã tồn tại",
            )

        admin_user_document = AdminUserModel(
            full_name=body.full_name,
            email=body.email,
            phone=body.phone,
            password_hash=hash_password(body.password),
            is_active=True,
            is_poi_owner_verified=False,
            id_card_encrypted=encrypt_pii(body.id_card),
            pii_collected_at=datetime.now(timezone.utc),
        ).to_dump()

        admin_user_inserted = await self.admin_user_repository.insert(
            admin_user_document
        )

        poi_owner_registration_document = PoiOwnerRegistrationModel(
            user_id=admin_user_inserted.inserted_id,
            business_name=body.business_name,
            business_address=body.business_address,
            admin_note="",
            status=PoiOwnerRegistrationStatus.PENDING,
        ).to_dump()

        poi_owner_registration_inserted = (
            await self.poi_owner_registration_repository.insert(
                poi_owner_registration_document
            )
        )

        return {
            "admin_user_id": str(admin_user_inserted.inserted_id),
            "poi_owner_registration_id": str(
                poi_owner_registration_inserted.inserted_id
            ),
        }

    async def login(self, body: Login):
        identifier = body.identifier.strip()
        existing = await self.admin_user_repository.find_by_search(
            {
                "$or": [
                    {"email": identifier.lower()},
                    {"phone": identifier},
                ]
            }
        )

        if existing is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tài khoản không tồn tại",
            )

        if not compare_password(body.password, existing.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Thông tin đăng nhập không chính xác",
            )

        if not existing.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Tài khoản bị khóa",
            )

        if existing.role_id is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tài khoản chưa được cấp quyền",
            )

        role = await self.role_repository.find_by_id(existing.role_id)

        if role is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy quyền tài khoản",
            )

        access_token = generate_access_token(
            str(existing.id),
            role.name,
            role.permissions,
            existing.is_poi_owner_verified,
        )
        refresh_token = generate_refresh_token(str(existing.id))

        return {"access_token": access_token, "refresh_token": refresh_token}
