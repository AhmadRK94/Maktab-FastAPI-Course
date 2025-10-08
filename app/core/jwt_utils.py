import jwt
from datetime import datetime, timedelta
from app.core.config import config
from jwt.exceptions import DecodeError, InvalidSignatureError
from fastapi import HTTPException, status


def generate_access_token(
    user_id: int, expires_in: int = config.ACCESS_TOKEN_EXPIRE_MINUTES
) -> str:
    now = datetime.now()
    iat = int(now.timestamp())
    exp = int((now + timedelta(minutes=expires_in)).timestamp())
    payload = {
        "type": "access",
        "user_id": user_id,
        "iat": iat,
        "exp": exp,
    }
    return jwt.encode(
        payload=payload, key=config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM
    )


def generate_refresh_token(
    user_id: int, expires_in: int = config.REFRESH_TOKEN_EXPIRE_DAYS
) -> str:
    now = datetime.now()
    iat = int(now.timestamp())
    exp = int((now + timedelta(days=expires_in)).timestamp())
    payload = {
        "type": "refresh",
        "user_id": user_id,
        "iat": iat,
        "exp": exp,
    }
    return jwt.encode(
        payload=payload, key=config.JWT_SECRET_KEY, algorithm=config.JWT_ALGORITHM
    )


## decode and verify the token + all the error handling
def decode_verify_token(token: str, token_type: str = "access") -> dict:
    try:
        payload = jwt.decode(
            token, config.JWT_SECRET_KEY, algorithms=[config.JWT_ALGORITHM]
        )
        if payload.get("type") != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed, Invalid token type.",
            )
        if datetime.now().timestamp() > payload.get("exp"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed, token expired.",
            )
        user_id = payload.get("user_id", None)
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed, user id not in the payload.",
            )
        return payload
    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed, Decode failed.",
        )
    except InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed, Invalid signature.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed, {e}",
        )
