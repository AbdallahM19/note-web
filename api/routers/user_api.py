"""user_api.py"""

from typing import Union, Optional, Annotated
from uuid import uuid4
from re import match
from fastapi import APIRouter, HTTPException, Path, Depends, Body, Request, status, Form,\
    File, UploadFile
from fastapi.responses import RedirectResponse, FileResponse
from api.app import user_model
from api.database import UserDb
from api.models.users import BaseUser, UserIn, UserField
from api.utils.session import SessionManager, get_session_manager, clear_session


router = APIRouter(
    prefix='/api/users',
    tags=['user-api']
)

EMAIL_REGEX = r"^([a-z]+)((([a-z]+)|(_[a-z]+))?(([0-9]+)|(_[0-9]+))?)*@([a-z]+).([a-z]+)$"


@router.get("/{field}")
async def get_user(
    # req: Request,
    field: UserField,
    user_id: Union[int, str] = None,
    name: Optional[str] = None,
    skip: Optional[int] = None,
    limit: Optional[int] = None,
    session: SessionManager = Depends(get_session_manager)
) -> Union[str, BaseUser, list[BaseUser]]:
    """
    Get user by id, or
    get all users with optional filtering and pagination.
    """
    users_data: Union[str, dict, list, None] = None

    match field:
        case "me":
            users_data = user_model.get_user_by_id(session.user_id)
        case "id":
            if isinstance(user_id, int):
                users_data = user_model.get_user_by_id(user_id)
            elif isinstance(user_id, str) and user_id == "me":
                users_data = user_model.get_user_by_id(session.user_id)
            elif isinstance(user_id, str) and user_id.isdigit():
                users_data = user_model.get_user_by_id(int(user_id))
        case "name" if name:
            users_data = user_model.get_user_by_username(name, skip, limit)
        case "list":
            users_data = user_model.get_all_users_data(skip, limit)
        case _:
            users_data = f"Invalid field: '{field}'."

    if not users_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if isinstance(users_data, UserDb):
        return users_data

    if isinstance(users_data, list):
        if len(users_data) == 1:
            return users_data
        return users_data

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=users_data
    )


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login(
    req: Request,
    username: Annotated[str, Form(min_length=3, max_length=100)],
    password: Annotated[str, Form()]
) -> BaseUser:
    """Login a user and set session data."""
    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username or email is required"
        )

    email = None

    if match(EMAIL_REGEX, username):
        email = username
        username = None

    try:
        current_user = user_model.check_if_user_exists(username=username, email=email)

        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid username or email. user not found"
            )

        if current_user.hashed_password != password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password. password not correct"
            )

        # Set session data for authenticated user
        req.session["id"] = current_user.id
        req.session["session_id"] = current_user.session_id

        # return current_user
        return RedirectResponse(url="/home", status_code=302)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while logging the user: {str(e)}"
        ) from e


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    req: Request,
    username: Annotated[str, Form(min_length=3, max_length=50)],
    email: Annotated[str, Form(
        max_length=100,
        pattern=EMAIL_REGEX
    )],
    password: Annotated[str, Form()],
) -> BaseUser:
    """Register a new user"""
    try:
        existing_user = user_model.check_if_user_exists(username, email)

        if existing_user:
            error_field = "username" if existing_user.username == username else "email"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User already exists. Please try with different {error_field}"
            )

        # Insert new user and set session details
        current_user = user_model.insert_new_user(
            username=username,
            email=email,
            hashed_password=password,
            # date_of_birth=date_of_birth,
            session_id=str(uuid4())
        )

        req.session["id"] = current_user.id
        req.session["session_id"] = current_user.session_id

        # return current_user
        return RedirectResponse(url="/home", status_code=302)
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while registering the user: {str(e)}"
        ) from e


@router.put("/{user_id}/update", status_code=status.HTTP_200_OK)
async def update_user_data(
    user_id: Annotated[
        Union[int, str], Path(
            title="Update user by id or 'me'",
            description="Update user data by id or 'me' to update current user data",
            examples=[
                {
                    "user_id": 19
                },
                {
                    "user_id": "me"
                }
            ]
        )
    ],
    user_account: Annotated[
        UserIn,
        Body(
            examples=[
                {
                    "username": "Mohamed",
                    "email": "mohammed123@example.com",
                    "hashed_password": "mohammed@123",
                    "date_of_birth": "11-1-2002",
                },
                {
                    "username": "john",
                    "email": "johnJ2@example.com",
                    "hashed_password": "johnJ2@123",
                    "date_of_birth": "",
                },
                {
                    "username": "alex",
                    "email": "alex123@example.com",
                    "hashed_password": "alexA",
                    "date_of_birth": "24-5-2002",
                },
                {
                    "username": "alex",
                    "email": "alex123@example.com",
                    "hashed_password": "alexA",
                    "date_of_birth": "",
                }
            ]
        )
    ],
    session: SessionManager = Depends(get_session_manager)
) -> dict:
    """Update user Account"""
    try:
        if isinstance(user_id, str) and user_id.isdigit():
            user_id = int(user_id)

        user_dict = user_account.model_dump()

        if isinstance(user_id, int) and user_id >= 1:
            user_dict["id"] = user_id
        elif isinstance(user_id, str) and user_id == 'me':
            user_dict["session_id"] = session.session_id
            # user_dict["id"] = session.user_id
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user_id. It should be either 'me' or a positive integer."
            )

        if user_model.update_user_account(user_dict):
            return {
                "message": "User data updated successfully",
                "user_data": BaseUser(
                    username=user_dict["username"],
                    email=user_dict["email"],
                    date_of_birth=user_dict["date_of_birth"],
                ),
                # "status": 200
            }
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update user account id={user_id}"
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the user: {str(e)}"
        ) from e


@router.get("/{user_id}/profile-image")
async def get_user_profile_image(
    user_id: Annotated[
        Union[int, str], Path(
            title="Update user by id or 'me'",
            description="Update user data by id or 'me' to update current user data",
            examples=[{"user_id": 19}, {"user_id": "me"}]
        )
    ],
    session: SessionManager = Depends(get_session_manager)
):
    """Get user profile image"""
    try:
        if isinstance(user_id, str) and user_id.isdigit():
            user_id = int(user_id)

        if user_id == "me":
            user_id = session.user_id

        location_file = await user_model.load_user_profile_image(user_id)

        if location_file:
            return FileResponse(location_file, media_type="image/jpeg")
            # return Response(content=open(location_file, 'rb').read(), media_type="image/jpeg")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile image not found"
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while getting the user profile image: {str(e)}"
        ) from e


@router.post("/{user_id}/profile-image", status_code=status.HTTP_201_CREATED)
async def update_user_profile_image(
    user_id: Annotated[
        Union[int, str], Path(
            title="Update user by id or 'me'",
            description="Update user data by id or 'me' to update current user data",
            examples=[{"user_id": 19}, {"user_id": "me"}]
        )
    ],
    file: Annotated[
        UploadFile, File(
            title="Profile image",
            description="Profile image to be uploaded",
            examples=[{"image": "image.jpg"}]
        )
    ],
    session: SessionManager = Depends(get_session_manager)
):
    """Update user profile image"""
    try:
        if isinstance(user_id, str) and user_id.isdigit():
            user_id = int(user_id)

        if user_id == "me":
            user_id = session.user_id

        location_file = await user_model.create_dir_if_not_exists(user_id, file)

        if location_file:
            return {
                "message": "Profile image updated successfully",
                "profile_image": location_file,
                # "status": 200
            }
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile image"
        )
    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the profile image: {str(e)}"
        ) from e


@router.delete("/{user_id}/delete")
async def delete_user_account_completely(
    user_id: Annotated[
        Union[str, int], Path(
            title="The ID of the user to delete.",
            description="This will delete the user account completely.",
            examples=[{"user_id": 19}, {"user_id": "me"}]
        )
    ],
    req: Request
) -> dict:
    """Delete user Account permanently"""
    if isinstance(user_id, str) and user_id == "me":
        user_id = req.session.get("id")
        await clear_session(req)

    if user_model.delete_user(user_id):
        return {
            "message": "User account has been deleted successfully",
        }

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Failed to delete user account id={user_id}"
    )


@router.delete("/logout")
async def logout_user(_: None = Depends(clear_session)):
    """Logout user"""
    return RedirectResponse(url="/login", status_code=303)
