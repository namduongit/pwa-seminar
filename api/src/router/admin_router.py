from typing import Annotated

from fastapi import APIRouter, Depends

from core.api_response import ApiResponse
from schema.admin_schema import AdminUserFilter, UpdatePoiPOwnerRegistration
from service.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin Controller"])


# interaction document - collection: poi_owner_registration
@router.patch("/registrations/{registration_id}")
async def review_registration(
    registration_id: str,
    body: UpdatePoiPOwnerRegistration,
    admin_service: Annotated[AdminService, Depends()],
) -> ApiResponse[dict]:
    result = await admin_service.review_registration(registration_id, body)

    return ApiResponse(
        success=True,
        message="Cập nhật đơn đăng ký thành công",
        data=result,
    )


# dependencies=[Depends(require_permission("user:read"))]
# interact document - collection: admin_user
@router.get("/admin-users")
async def filter_admin_users(
    filters: Annotated[AdminUserFilter, Depends()],
    admin_service: Annotated[AdminService, Depends()],
):
    _ = await admin_service.filter_admin_users(filters)
