from fastapi import Request, HTTPException, status, Depends
from app.core.db import get_db, Session
from app.users.models import UserModel
from app.core.jwt_utils import decode_verify_token


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
) -> UserModel:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed, access token not found.",
        )
    decoded_token = decode_verify_token(token, token_type="access")
    user_object = db.query(UserModel).filter_by(id=decoded_token.get("user_id")).one()

    return user_object
