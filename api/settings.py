from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from api.utils.session import SessionManager, get_session_manager
from functools import wraps


def load_current_user(func):
    @wraps(func)
    async def wrapper(req: Request, *args, **kwargs):
        session_manager: SessionManager = await get_session_manager(req)

        if session_manager.user_id or session_manager.session_id:
            return RedirectResponse(
                url="/home",
                status_code=302,
            )
        return await func(req, *args, **kwargs)
    return wrapper
