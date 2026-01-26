from http import HTTPStatus
from typing import Dict, Any


class HTTPException(Exception):
    def __init__(self, status: HTTPStatus, message: str):
        self.status = status
        self.message = message

    def to_dict(self) -> Dict[str, Any]:
        return {"status": self.status, "message": self.message}


class BadRequestException(HTTPException):
    def __init__(self, message: str = "Bad Request"):
        super().__init__(HTTPStatus.BAD_REQUEST, message)


class UnauthorizedException(HTTPException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(HTTPStatus.UNAUTHORIZED, message)


class ForbiddenException(HTTPException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(HTTPStatus.FORBIDDEN, message)


class NotFoundException(HTTPException):
    def __init__(self, message: str = "Not Found"):
        super().__init__(HTTPStatus.NOT_FOUND, message)


class ConflictException(HTTPException):
    def __init__(self, message: str = "Conflict"):
        super().__init__(HTTPStatus.CONFLICT, message)


class InternalServerErrorException(HTTPException):
    def __init__(self, message: str = "Internal Server Error"):
        super().__init__(HTTPStatus.INTERNAL_SERVER_ERROR, message)
