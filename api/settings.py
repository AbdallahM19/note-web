from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from api.utils.session import SessionManager, get_session_manager
from functools import wraps


def load_current_user(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        req = kwargs.get("req") or (args[0] if args and isinstance(args[0], Request) else None)
        if not req:
            raise HTTPException(
                status_code=401,
                detail="Missing request object",
            )

        session_manager: SessionManager = await get_session_manager(req)

        if session_manager.user_id or session_manager.session_id:
            return RedirectResponse(
                url="/home",
                status_code=302,
            )
        return await func(*args, **kwargs)
    return wrapper


def require_login(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        req = kwargs.get("req") or (args[0] if args and isinstance(args[0], Request) else None)
        if not req:
            raise HTTPException(
                status_code=401,
                detail="Missing request object",
            )

        session_manager: SessionManager = await get_session_manager(req)

        print("------------------------------")
        print(f"Current user: {"Existing" if session_manager.session_id or session_manager.user_id else 'No user'}")
        print("------------------------------")

        if not (session_manager.user_id or session_manager.session_id):
            return RedirectResponse(
                url="/login",
                status_code=302,
            )
        return await func(*args, **kwargs)
    return wrapper
