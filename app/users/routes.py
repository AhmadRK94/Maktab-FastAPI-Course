from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.users.schemas import UserRegisterSchema, UserResponseSchema
from app.core.db import Session, get_db
from app.users.models import UserModel

router = APIRouter(prefix="/users", tags=["users"])


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=list[UserResponseSchema]
)
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(UserModel).all()
    return users


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(request: UserRegisterSchema, db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(email=request.email.lower()).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email: {request.email.lower()} is already exist.",
        )
    user_object = UserModel(username=request.username, email=request.email.lower())
    user_object.set_password(request.password)
    db.add(user_object)
    db.commit()
    return JSONResponse(
        content={
            "detail": "User registered successfully.",
        }
    )
