from pydantic import BaseModel, Field, EmailStr, field_validator


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(..., max_length=150, description="email of the user")
    password: str = Field(..., description="password of the user")


class UserRegisterSchema(BaseModel):
    email: EmailStr = Field(..., max_length=150, description="email of the user")
    password: str = Field(..., description="password of the user")
    password_confirm: str = Field(..., description="user password confirmation")
    username: str = Field(..., description="username of the user")

    @field_validator("password_confirm")
    def check_password_match(cls, password_confirm, validation):
        if not validation.data.get("password") == password_confirm:
            raise ValueError("Passwords don't match.")
        return password_confirm


class UserResponseSchema(BaseModel):
    id: int = Field(..., description="user id.")
    username: str = Field(..., description="username of the user")
    email: EmailStr = Field(..., max_length=150, description="email of the user")

    # class Config:
    #     orm_mode = True
