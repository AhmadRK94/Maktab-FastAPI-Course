from fastapi import APIRouter, status, HTTPException, Depends, Request, Query
from fastapi.responses import (
    JSONResponse,
)  ## inherit from Response class so we can set cookies using it

from app.auth.schemas import UserLoginSchema
from app.core.db import Session, get_db
from app.users.models import UserModel
from app.core.cookie_utils import set_access_cookie, set_refresh_cookie, clear_cookies
from app.core.jwt_utils import (
    generate_access_token,
    generate_refresh_token,
    decode_verify_token,
)
from app.dependencies.i18n import get_translator

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(
    request: UserLoginSchema,
    db: Session = Depends(get_db),
    _=Depends(get_translator),
    lang: str = Query(default="en"),
):
    user_object = db.query(UserModel).filter_by(email=request.email.lower()).first()
    if not user_object:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_("Invalid Username or Password."),
        )
    if not user_object.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=_("Invalid Username or Password."),
        )
    response = JSONResponse(content={"detail": _("Login successful.")})
    access_token = generate_access_token(user_object.id)
    refresh_token = generate_refresh_token(user_object.id)

    set_access_cookie(response, access_token)
    set_refresh_cookie(response, refresh_token)
    return response


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout_user(_=Depends(get_translator), lang: str = Query(default="en")):
    response = JSONResponse(content={"detail": _("Logout successful.")})
    clear_cookies(response)
    return response


@router.post("/refresh-token", status_code=status.HTTP_200_OK)
def refresh_access_token(
    request: Request, _=Depends(get_translator), lang: str = Query(default="en")
):
    refresh_token = request.cookies.get("refresh_token", None)
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=_("Authentication failed, refresh token not found."),
        )

    payload = decode_verify_token(refresh_token, token_type="refresh")
    user_id = payload.get("user_id")
    new_access_token = generate_access_token(user_id)
    response = JSONResponse(
        content={"detail": _("Access token refreshed successfully.")}
    )
    set_access_cookie(response, new_access_token)
    return response
