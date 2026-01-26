from pydantic import BaseModel, Field

from src.modules.user.user_dto import UsersResponseDto


class SigninDto(BaseModel):
    email: str = Field(..., format="email", description="Email")
    password: str = Field(..., min_length=8, description="Password")


class SignupDto(BaseModel):
    fullname: str = Field(..., min_length=3, description="Full Name")
    email: str = Field(..., format="email", description="Email")
    password: str = Field(..., min_length=8, description="Password")
    confirm_password: str = Field(..., min_length=8, description="Confirm Password")


class ForgotPasswordDto(BaseModel):
    email: str = Field(..., format="email", description="Email")


class ResetPasswordDto(BaseModel):
    reset_token: str = Field(..., description="Reset Token")
    password: str = Field(..., min_length=8, description="Password")
    confirm_password: str = Field(..., min_length=8, description="Confirm Password")
