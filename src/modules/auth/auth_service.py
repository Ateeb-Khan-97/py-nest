from datetime import datetime, timezone, timedelta
from typing import Dict
from fastapi import Response
from nest.core import Injectable
from jose import jwt, JWTError

from src.config.env_config import env
from src.modules.auth.auth_enum import TokenType


@Injectable()
class AuthService:
    SECRETS: Dict[TokenType, str] = {
        TokenType.ACCESS: env.JWT_ACCESS_TOKEN_SECRET,
        TokenType.REFRESH: env.JWT_REFRESH_TOKEN_SECRET,
        TokenType.RESET_PASSWORD: env.JWT_RESET_PASSWORD_TOKEN_SECRET,
    }
    EXPIRY_MINUTES: Dict[TokenType, int] = {
        TokenType.ACCESS: env.JWT_ACCESS_TOKEN_EXPIRY_MINUTES,
        TokenType.REFRESH: env.JWT_REFRESH_TOKEN_EXPIRY_MINUTES,
        TokenType.RESET_PASSWORD: env.JWT_RESET_PASSWORD_TOKEN_EXPIRY_MINUTES,
    }

    def create_token(self, user_id: int, token_type: TokenType) -> str:
        now = int(datetime.now(timezone.utc).timestamp())
        expiry_seconds = self.EXPIRY_MINUTES[token_type] * 60
        expiry = now + expiry_seconds

        payload = {
            "sub": str(user_id),
            "exp": expiry,
            "iat": now,
            "nbf": now,
            "type": token_type.value,
        }
        print(f"Creating {token_type.value} token: now={now}, exp={expiry}")
        token = jwt.encode(payload, self.SECRETS[token_type], algorithm="HS256")
        return token

    def create_auth_tokens(self, user_id: int) -> tuple[str, str]:
        return (
            self.create_token(user_id, TokenType.ACCESS),
            self.create_token(user_id, TokenType.REFRESH),
        )

    def validate_token(self, token: str, token_type: TokenType) -> int | None:
        try:
            # Debug: Check what's inside the token without verification
            unverified = jwt.get_unverified_claims(token)
            print(f"Validating {token_type.value} token: {unverified}")
            print(f"Current UTC: {int(datetime.now(timezone.utc).timestamp())}")

            payload = jwt.decode(
                token,
                self.SECRETS[token_type],
                algorithms=["HS256"],
                options={"leeway": 60},
            )
            if payload.get("type") != token_type.value:
                print(f"Type mismatch: expected {token_type.value}, got {payload.get('type')}")
                return None
            try:
                return int(payload.get("sub"))
            except (ValueError, TypeError):
                return None
        except JWTError as e:
            print("JWTError", e)
            return None

    def login(self, user_id: int, response: Response) -> Response:
        access_token, refresh_token = self.create_auth_tokens(user_id)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=env.JWT_ACCESS_TOKEN_EXPIRY_MINUTES * 60,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=env.JWT_REFRESH_TOKEN_EXPIRY_MINUTES * 60,
        )
        return response
