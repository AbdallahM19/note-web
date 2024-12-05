"""app.py"""

from typing import Union
from fastapi import APIRouter
from pydantic import BaseModel
from api.models.users import User
from api.models.notes import Note


router = APIRouter()
user_model = User()
note_model = Note()


class Test(BaseModel):
    """Test class to test the API endpoints"""
    title: Union[str, None]
    search: Union[set, None]


@router.get("/")
async def root():
    """root"""
    return {"message": "Hello World"}


@router.get("/home")
async def home():
    """Home Page"""
    return {"message": "Welcome in Home"}


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


@router.put("/index")
async def index(items: Test):
    """index Page"""
    print(
        f"\n\nTitle: {items.title}\nSearch: {items.search}\n\n"
    )

# @router.get("/register")
# for get html register


# @router.get("/login")
# for get html login
