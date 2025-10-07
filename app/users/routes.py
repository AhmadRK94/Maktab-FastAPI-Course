from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse

from app.users.schemas import UserLoginSchema, UserRegisterSchema, UserResponseSchema
from app.core.db import Session, get_db
from app.users.models import UserModel

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(request: UserLoginSchema, db: Session = Depends(get_db)):
    user_object = db.query(UserModel).filter_by(email=request.email.lower()).first()
    if not user_object:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Username or Password.",
        )
    if not user_object.verify_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid Username or Password.",
        )
    return JSONResponse(
        content={
            "detail": "Logged in successfully.",
        }
    )


@router.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=UserResponseSchema
)
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
            # "user": UserResponseSchema.model_validate(user_object).model_dump(),
        }
    )
