from typing import Annotated

from core.api_response import ApiResponse
from core.dependency import AccessTokenPayload, require_permission
from fastapi import APIRouter, Depends
from service.owner_service import OwnerService

router = APIRouter(prefix="/owner", tags=["Owner Controller"])


@router.get("/registration-status")
async def get_registration_status(
    state: Annotated[AccessTokenPayload, Depends(require_permission("owner:access"))],
    owner_service: Annotated[OwnerService, Depends()],
):
    poi_owner_registration = await owner_service.get_registration_status(state.sub)

    return ApiResponse(
        success=True,
        message="Lấy dữ liệu thành công",
        data={
            "registration_id": str(poi_owner_registration.id),
            "user_id": str(poi_owner_registration.user_id),
            "business_name": poi_owner_registration.business_name,
            "business_address": poi_owner_registration.business_address,
            "status": poi_owner_registration.status,
            "admin_note": poi_owner_registration.admin_note or None,
            "is_poi_owner_verified": state.is_poi_owner_verified,
        },
    )


@router.get("/dashboard")
async def get_owner_dashboard():
    pass


@router.get("/pois")
async def get_owner_pois():
    pass


@router.get("/pois/{poi_id}")
async def get_owner_poi(poi_id: str):
    pass


@router.put("/pois/{poi_id}")
async def update_owner_poi(poi_id: str):
    pass


@router.get("/submissions")
async def get_owner_submissions():
    pass


@router.post("/submissions")
async def create_owner_submission():
    pass


@router.get("/submissions/{submission_id}")
async def get_owner_submission(submission_id: str):
    pass


@router.get("/notifications")
async def get_owner_notifications():
    pass


@router.get("/notifications/unread-count")
async def get_unread_notification_count():
    pass


@router.get("/notifications/{notification_id}")
async def get_owner_notification(notification_id: str):
    pass


@router.patch("/notifications/{notification_id}/read")
async def mark_owner_notification_as_read(notification_id: str):
    pass
