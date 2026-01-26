from nest.core import Controller, Get, Put, UseGuards
from src.core.exceptions.http_exceptions import NotFoundException
from src.core.guards.bearer_guard import BearerTokenGuard
from src.core.dependencies.current_user import CurrentUser
from src.modules.user.user_service import UserService
from src.core.mappers.response_mapper import BaseResponse, ResponseMapper
from src.modules.user.user_dto import UsersResponseDto, UsersUpdateDto


@Controller("/user", tag="User")
class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @UseGuards(BearerTokenGuard)
    @Get("/profile", response_model=BaseResponse[UsersResponseDto])
    async def fetch_profile_handler(self, user_id: CurrentUser):
        user = await self.user_service.find_one_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        return ResponseMapper(
            data=user.model_dump(exclude={"password", "deleted_at"}),
            message="Profile fetched successfully",
        )

    @UseGuards(BearerTokenGuard)
    @Put("/profile", response_model=BaseResponse[UsersResponseDto])
    async def update_profile_handler(self, user_id: CurrentUser, body: UsersUpdateDto):
        user = await self.user_service.find_one_by_id(user_id)
        if not user:
            raise NotFoundException("User not found")
        user = await self.user_service.update(user_id, body.model_dump())
        return ResponseMapper(
            data=user.model_dump(exclude={"password", "deleted_at"}),
            message="Profile updated successfully",
        )
