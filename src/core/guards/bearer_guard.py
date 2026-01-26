from fastapi import Request
from fastapi.security import HTTPBearer
from nest.core import BaseGuard

from src.core.exceptions.http_exceptions import UnauthorizedException
from src.modules.auth.auth_enum import TokenType
from src.modules.auth.auth_service import AuthService

_auth_service = AuthService()


class BearerTokenGuard(BaseGuard):
    security_scheme = HTTPBearer(description="Bearer token")

    def __init__(self):
        self.auth_service = _auth_service

    def can_activate(self, request: Request, credentials=None) -> bool:
        # 1. Try Bearer Token in Header
        if credentials and credentials.scheme == "Bearer":
            user_id = self.auth_service.validate_token(
                credentials.credentials, TokenType.ACCESS
            )
            if user_id is not None:
                request.state.user_id = user_id
                return True

        # 2. Try access_token in Cookies
        token = request.cookies.get("access_token")
        if token:
            user_id = self.auth_service.validate_token(token, TokenType.ACCESS)
            if user_id is not None:
                request.state.user_id = user_id
                return True

        raise UnauthorizedException("Missing or invalid authentication token")

    def validate_jwt_token(self, request: Request, token: str) -> bool:
        # This method is now redundant but kept for backward compatibility if used elsewhere
        user_id = self.auth_service.validate_token(token, TokenType.ACCESS)
        if user_id is not None:
            request.state.user_id = user_id
            return True

        raise UnauthorizedException("Invalid token payload")
