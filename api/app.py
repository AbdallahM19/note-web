"""app.py"""

from typing import Union
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from api.settings import SessionHandler
from api.models.users import User
from api.models.notes import Note


router = APIRouter()
user_model = User()
note_model = Note()

templates = Jinja2Templates(directory="templates")


class Test(BaseModel):
    """Test class to test the API endpoints"""
    title: Union[str, None]
    search: Union[set, None]


@router.get("/")
async def root():
    """root"""
    return {
        "message": "Hello World"
    }


@router.get("/home")
@SessionHandler(action="require_login")
async def home(req: Request):
    """Home Page"""
    current_user = user_model.get_user_by_session_id(
        req.session.get("session_id")
    )
    return {
        "message": f"Welcome {current_user.username} in Home"
    }


@router.get("/register", response_class=HTMLResponse)
@SessionHandler(action="load_current_user")
async def register(req: Request):
    """Register Page"""
    return templates.TemplateResponse(
        request = req,
        name = "login_page.html",
        context = {
            "title": "Register Page",
            "types_container": "sign-up-mode signup-mode2",
        }
    )


@router.get("/login", response_class=HTMLResponse)
@SessionHandler(action="load_current_user")
async def login(req: Request):
    """Login Page"""
    return templates.TemplateResponse(
        request = req,
        name = "login_page.html",
        context = {
            "title": "Login Page",
            "types_container": "",
        }
    )


@router.get("/index")
async def index():
    """index Page"""
    content = """
        <body>
            <img src="/api/users/me/profile-image">
        </body>
    """
    return HTMLResponse(content=content)


# @router.put("/index")
# async def index(items: Test):
#     """index Page"""
#     print(
#         f"\n\nTitle: {items.title}\nSearch: {items.search}\n\n"
#     )


# @router.get("/index")
# async def index(
#     id: Union[int, None]
#     name: Annotated[Optional[str], Query(min_length=10, max_length=50)] = None,
#     # name: Annotated[Optional[list[str]], Query()] = None,
#     # name: Annotated[Optional[list[int]], Query()] = None,
#     # search: Annotated[Optional[str], Query(title="Search Field", min_length=3)] = None,
#     search: Annotated[Optional[str], Path(title="Search Field")] = None,
#     request: Request,
# ):
#     """index Page"""
#     print()
