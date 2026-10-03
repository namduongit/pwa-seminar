from typing import Annotated

from core.api_response import ApiResponse
from fastapi import APIRouter, Depends
from schema.admin_schema import UpdatePoiPOwnerRegistration
from service.admin_service import AdminService

router = APIRouter(prefix="/admin", tags=["Admin Controller"])


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
