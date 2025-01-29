"""session.py"""

from fastapi import Request


class SessionManager:
    """Session manager for FastAPI."""
    def __init__(self, user_id: int = None, session_id: str = None):
        self.user_id = user_id
        self.session_id = session_id

    @classmethod
    async def get_session_id(cls, request: Request):
        """Get session id from session object."""
        return cls(
            user_id=request.session.get("id"),
            session_id=request.session.get("session_id")
        )


async def get_session_manager(request: Request) -> SessionManager:
    """Get session manager instance from request."""
    return await SessionManager.get_session_id(request)

async def get_current_user_id(request: Request) -> int:
    """Get session manager instance from request."""
    session = await SessionManager.get_session_id(request)
    return session.user_id

async def get_current_session_id(request: Request) -> str:
    """Get session manager instance from request."""
    session = await SessionManager.get_session_id(request)
    return session.session_id
