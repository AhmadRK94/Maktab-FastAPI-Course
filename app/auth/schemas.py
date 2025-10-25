from pydantic import BaseModel, Field, EmailStr


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(..., max_length=150, description="email of the user")
    password: str = Field(..., description="password of the user")
