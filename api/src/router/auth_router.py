from typing import Annotated

from core.api_response import ApiResponse
from core.dependency import AccessTokenPayload, get_current_access_token
from fastapi import APIRouter, Depends, Request, Response
from schema.auth_schema import ChangePassword, Login, RegisterPoiOwner
from service.auth_service import AuthService

router = APIRouter(prefix="/admin/auth", tags=["Admin Auth Controller"])


@router.post("/register-owner")
async def register_poi_owner(
    body: RegisterPoiOwner,
    auth_service: Annotated[AuthService, Depends()],
) -> ApiResponse[dict[str, str]]:

    result = await auth_service.register_poi_owner(body)
    return ApiResponse(success=True, message="Đăng ký chủ quán thành công", data=result)


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
async def refresh_token(
    request: Request,
    response: Response,
    auth_service: Annotated[AuthService, Depends()],
) -> ApiResponse[None]:
    access_token = await auth_service.refresh_access_token(
        request.cookies.get("refresh_token")
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=30 * 60,
        path="/",
    )

    return ApiResponse(
        success=True,
        message="Làm mới phiên đăng nhập thành công",
    )


@router.post("/logout")
async def logout(response: Response) -> ApiResponse[None]:
    response.delete_cookie(key="access_token", path="/")
    response.delete_cookie(key="refresh_token", path="/admin/auth")

    return ApiResponse(
        success=True,
        message="Đăng xuất thành công",
    )


@router.post("/change-password")
async def change_password(
    body: ChangePassword,
    state: Annotated[AccessTokenPayload, Depends(get_current_access_token)],
    auth_service: Annotated[AuthService, Depends()],
) -> ApiResponse[None]:
    await auth_service.change_password(state.sub, body)

    return ApiResponse(
        success=True,
        message="Đổi mật khẩu thành công",
    )
