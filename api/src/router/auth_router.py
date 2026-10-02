from typing import Annotated

from core.api_response import ApiResponse
from fastapi import APIRouter, Depends, Response
from schema.auth_schema import Login, RegisterPoiOwner
from service.auth_service import AuthService

router = APIRouter(prefix="/admin/auth", tags=["Admin Auth Controller"])


@router.get("/check-health")
def check_health(
    auth_service: Annotated[AuthService, Depends()],
) -> ApiResponse[dict[str, bool]]:
    return ApiResponse(
        success=True,
        message="Auth service hoạt động",
        data={"healthy": auth_service is not None},
    )


@router.post("/register-owner")
async def register_poi_owner(
    body: RegisterPoiOwner,
    auth_service: Annotated[AuthService, Depends()],
) -> ApiResponse[dict[str, str]]:

    result = await auth_service.register_poi_owner(body)
    return ApiResponse(
        success=True,
        message="Đăng ký chủ quán thành công",
        data=result,
    )


@router.post("/login")
async def login(
    body: Login, auth_service: Annotated[AuthService, Depends()], response: Response
) -> ApiResponse[None]:
    result = await auth_service.login(body)

    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=30 * 60,
        path="/",
    )

    response.set_cookie(
        key="refresh_token",
        value=result["refresh_token"],
        httponly=True,
        secure=False,  # Local HTTP
        samesite="lax",
        max_age=7 * 24 * 60 * 60,
        path="/admin/auth",
    )

    return ApiResponse(
        success=True,
        message="Đăng nhập thành công",
    )


@router.get("/me")
async def get_current_user():
    pass


@router.post("/refresh")
async def refresh_token():
    pass


@router.post("/logout")
async def logout():
    pass


@router.post("/change-password")
async def change_password():
    pass

