from typing import Any
from datetime import datetime
from starlette.responses import JSONResponse
from pydantic import BaseModel


class BaseResponse[T: Any | None](BaseModel):
    success: bool = True
    status: int = 200
    message: str = "Success"
    data: T = None


def _serialize_datetime(obj: Any) -> Any:
    """Recursively convert datetime objects to ISO format strings."""
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {key: _serialize_datetime(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [_serialize_datetime(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(_serialize_datetime(item) for item in obj)
    return obj


def ResponseMapper(
    status: int = 200,
    message: str = "Success",
    data: Any = None,
) -> JSONResponse:
    # Serialize datetime objects in data
    serialized_data = _serialize_datetime(data) if data is not None else None

    content = {
        "success": status >= 200 and status < 300,
        "status": status,
        "message": message,
        "data": serialized_data,
    }

    return JSONResponse(
        status_code=status,
        content=content,
    )
