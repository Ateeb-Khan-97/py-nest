from typing import Annotated
from fastapi import Request, Depends
from src.core.exceptions.http_exceptions import UnauthorizedException


def get_current_user_id(request: Request) -> int:
    """
    Dependency to extract the current user ID from request state.
    This should be used after BearerTokenGuard has validated the token.
    
    Args:
        request: The FastAPI request object
        
    Returns:
        The user ID from the authenticated token
        
    Raises:
        UnauthorizedException: If user_id is not found in request state
    """
    user_id = getattr(request.state, "user_id", None)
    if user_id is None:
        raise UnauthorizedException("User not authenticated")
    return user_id


# Type alias for CurrentUser that can be used as a type annotation
CurrentUser = Annotated[int, Depends(get_current_user_id)]
