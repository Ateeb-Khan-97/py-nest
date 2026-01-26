from fastapi import Request
from nest.core import Controller, Post
from src.modules.auth.auth_dto import (
    ForgotPasswordDto,
    ResetPasswordDto,
    SigninDto,
    SignupDto,
)
from src.modules.auth.auth_enum import TokenType
from src.modules.auth.auth_service import AuthService
from src.modules.user.user_service import UserService
from src.modules.user.user_dto import UsersResponseDto
from src.core.exceptions.http_exceptions import (
    BadRequestException,
    ConflictException,
    NotFoundException,
    UnauthorizedException,
)
from src.core.mappers.response_mapper import BaseResponse, ResponseMapper


@Controller("/auth", tag="Auth")
class AuthController:
    def __init__(self, user_service: UserService, auth_service: AuthService):
        self.user_service = user_service
        self.auth_service = auth_service

    @Post("/sign-in", response_model=BaseResponse[UsersResponseDto])
    async def sign_in_handler(self, body: SigninDto):
        user = await self.user_service.find_one_by({"email": body.email})
        if not user or user.deleted_at is not None:
            raise NotFoundException("User not found")
        if not user.password == body.password:
            raise UnauthorizedException("Invalid credentials")

        response = ResponseMapper(
            data=user.model_dump(exclude={"password", "deleted_at"}),
            message="Signed in successfully",
        )
        return self.auth_service.login(user.id, response)

    @Post("/sign-up", response_model=BaseResponse[None], status_code=201)
    async def sign_up_handler(self, body: SignupDto):
        user = await self.user_service.find_one_by_email(body.email)
        if user:
            raise ConflictException("User already exists")
        if body.password != body.confirm_password:
            raise BadRequestException("Password and confirm password do not match")
        user = await self.user_service.create(
            user=body.model_dump(exclude={"confirm_password"})
        )
        return ResponseMapper(
            message="Signed up successfully",
            status=201,
        )

    @Post("/refresh-access", response_model=BaseResponse[None])
    async def refresh_access_handler(self, request: Request):
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            raise UnauthorizedException("Refresh token not found")

        user_id = self.auth_service.validate_token(refresh_token, TokenType.REFRESH)
        if not user_id:
            raise UnauthorizedException("Invalid refresh token")

        response = ResponseMapper(message="Session refreshed successfully")
        return self.auth_service.login(user_id, response)

    @Post("/sign-out", response_model=BaseResponse[None])
    async def logout_handler(self):
        response = ResponseMapper(message="Signed out successfully")
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response

    @Post("/forgot-password", response_model=BaseResponse[None])
    async def forgot_password_handler(self, body: ForgotPasswordDto):
        user = await self.user_service.find_one_by_email(body.email)
        if not user:
            raise NotFoundException("User not found")
        reset_password_token = self.auth_service.create_token(
            user.id, TokenType.RESET_PASSWORD
        )
        print(reset_password_token)
        # TODO: Send password reset email

        return ResponseMapper(message="Password reset email sent successfully")

    @Post("/reset-password", response_model=BaseResponse[None])
    async def reset_password_handler(self, body: ResetPasswordDto):
        user_id = self.auth_service.validate_token(
            body.reset_token, TokenType.RESET_PASSWORD
        )
        if not user_id:
            raise UnauthorizedException("Invalid reset token")
        if body.password != body.confirm_password:
            raise BadRequestException("Password and confirm password do not match")
        await self.user_service.update(user_id, {"password": body.password})
        return ResponseMapper(message="Password reset successfully")
