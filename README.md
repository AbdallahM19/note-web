# First Project Built with FastAPI

This FastAPI project provides endpoints for handling user accounts, including registration, login, data retrieval, updating, and deletion. The following documentation covers each route, its purpose, and example responses.

---

## API Documentation

### [General Routes](#route-definitions)
- [Root Route](#root-route)
- [Home Route](#home-route)

### [User Routes](#user-routes-1)
- [Get User](#get-user-route)
- [User Registration](#register-user-route)
- [User Login](#login-user-route)
- [Update User](#update-user-route)
- [Delete User](#delete-user-route)

### [Note Routes](#note-routes-1)
- [Get Notes](#get-notes-by-field)
- [Note Creation](#create-note)
- [Note Update](#update-note)
- [Delete Note](#delete-note)

### [Summary Table](#summary-table-1)

---

## Route Definitions

### Root Route
```python
@router.get("/")
async def root():
    """Root endpoint: Returns a simple greeting message."""
    return {"message": "Hello World"}
```
- **Path**: `/`
- **Description**: This is the root endpoint, used to confirm the API is active and running.
- **Response**: Returns a JSON object with a `message` key saying `"Hello World"`.
- **File**: [`/api/app.py`](./api/app.py)

### Home Route
```python
@router.get("/home")
async def home():
    """Home Page endpoint: Provides a welcome message for the home page."""
    return {"message": "Welcome in Home"}
```
- **Path**: `/home`
- **Description**: A simple route that provides a welcome message.
- **Response**: Returns a JSON object with a `message` key saying `"Welcome in Home"`.
- **File**: [`/api/app.py`](./api/app.py)

---

## User Routes

### Get User Route
```python
@router.get("/users/{field}")
async def get_user(
    field: Optional[str],
    user_id: Optional[int] = None,
    name: Optional[str] = None,
    skip: Optional[int] = None,
    limit: Optional[int] = None,
) -> Union[str, dict, list]:
    """Get user by ID or name, or list all users with optional pagination."""
```
- **Path**: `/api/users/{field}`
- **Description**: Retrieves user information based on specified `field`. Options include:
  - `"me"`: Returns data about the current user.
  - `"id"`: Retrieves user by `user_id`.
  - `"name"`: Retrieves user by `name` with optional pagination using `skip` and `limit`.
  - `"list"`: Retrieves all users with optional pagination.
- **Responses**: Returns JSON with user information or an error if not found.
- **File**: [`/api/routers/user_api.py`](./api/routers/user_api.py)

### Register User Route
```python
@router.post("/users/register")
async def register(
    username: Annotated[str, Query(min_length=3, max_length=50)],
    email: str, password: str, date_of_birth: Optional[str] = None,
    description: Annotated[Optional[str], Query(max_length=500)] = None
) -> dict:
    """Register a new user"""
```
- **Path**: `/api/users/register`
- **Description**: Registers a new user with a unique `username` and `email`. Optional fields include `date_of_birth` and a `description` with a 500-character limit.
- **Response**: Success response with the newly created user data or an error if the user already exists.
- **File**: [`/api/routers/user_api.py`](./api/routers/user_api.py)

### Login User Route
```python
@router.post("/users/login")
async def login(
    password: str,
    username: Annotated[Optional[str], Query(min_length=3, max_length=50)] = None,
    email: Annotated[Optional[str], Query(max_length=100)] = None,
) -> dict:
    """Login a user"""
```
- **Path**: `/api/users/login`
- **Description**: Authenticates a user by either `username` or `email` combined with a `password`. If successful, returns the user data.
- **Response**: Returns JSON indicating login success with user data or error messages for invalid credentials.
- **File**: [`/api/routers/user_api.py`](./api/routers/user_api.py)

### Update User Route
```python
@router.put("/users/{user_id}/update")
async def update_user_data(user_id: Union[int, str], user_account: UserAccount) -> dict:
    """Update user Account"""
```
- **Path**: `/api/users/{user_id}/update`
- **Description**: Update by user_id or 'me', that mean the current user.
- **Response**: Returns JSON with a success message and updated data, or an error if the update fails.
- **File**: [`/api/routers/user_api.py`](./api/routers/user_api.py)

### Delete User Route
```python
@router.delete("/users/{user_id}/delete")
async def delete_user_account_completely(user_id: int) -> dict:
    """Delete user Account permanently"""
```
- **Path**: `/api/users/{user_id}/delete`
- **Description**: Deletes a user account permanently based on the provided `user_id`.
- **Response**: Success message indicating account deletion, or error if deletion fails.
- **File**: [`/api/routers/user_api.py`](./api/routers/user_api.py)

### Logout User Route
```python
@router.post("/users/logout")
async def logout_user(session: SessionManager = Depends(get_session_manager)) -> dict:
    """Logout user"""
```
- **Path**: `/api/users/logout`
- **Description**: Logs out the current user by invalidating and clear their session.
- **Response**: Returns JSON indicating logout success with message User logged out successfully.
- **File**: [`/api/routers/user_api.py`](./api/routers/user_api.py)

---

## Note Routes

### Get Notes by Field

```python
@router.get("/notes/{field}")
async def get_notes_by_field(
    field: Optional[str],
    query: Optional[str] = None,
    note_id: Optional[int] = None,
    skip: Optional[int] = None,
    limit: Optional[int] = None,
) -> Union[list, dict]:
    """Get notes by field"""
```

- **Path**: `/notes/{field}`
- **Parameters**:
  - **field**: Specifies the field to filter by (e.g., `title`, `content`, `list`, or `id`).
  - **query**: (Optional) The search query for fields like `title` or `content`.
  - **note_id**: (Optional) If filtering by `id`, specifies the note's ID.
  - **skip** and **limit**: (Optional) Used for pagination.
- **Description**: This route fetches notes based on the specified field. It handles different fields with a `match` statement for specific cases like `id`, `title`, `content`, or listing all notes.
- **Response**: Returns a list of notes or an error message if an invalid field or query is provided.
- **File**: [`/api/routers/note_api.py`](./api/routers/note_api.py)

### Create Note

```python
@router.post("/notes/create")
async def create_note(
    user_id: int, content: str, title: Optional[str] = None
) -> dict:
    """Create a new note."""
```

- **Path**: `/notes/create`
- **Parameters**:
  - **user_id**: The ID of the user creating the note.
  - **content**: The content of the note.
  - **title**: (Optional) The title of the note.
- **Description**: Creates a new note associated with a user.
- **Response**: Returns a success message with the newly created note.
- **File**: [`/api/routers/note_api.py`](./api/routers/note_api.py)

### Update Note

```python
@router.put("/notes/{note_id}/update")
async def update_note(
    note_id: int,
    content: str,
    title: Optional[str] = None
) -> dict:
    """Update a note."""
```

- **Path**: `/notes/{note_id}/update`
- **Parameters**:
  - **note_id**: The ID of the note to be updated.
  - **content**: New content for the note.
  - **title**: (Optional) New title for the note.
- **Description**: Updates an existing note by its ID.
- **Response**: Returns the updated note details.
- **File**: [`/api/routers/note_api.py`](./api/routers/note_api.py)

### Delete Note

```python
@router.delete("/notes/{note_id}/delete")
async def delete_note_data_permanently(note_id: int) -> dict:
    """Delete note data permanently."""
```

- **Path**: `/notes/{note_id}/delete`
- **Parameters**:
  - **note_id**: The ID of the note to delete.
- **Description**: Permanently deletes a note by ID.
- **Response**: Returns a success message with the deleted note's ID.
- **File**: [`/api/routers/note_api.py`](./api/routers/note_api.py)

---

## Summary Table

| Route                     | Path                              | Description                                             | File                                                                                            |
|---------------------------|-----------------------------------|---------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| **Root**                  | `/`                               | API status check with a greeting message                | [`/api/app.py`](./api/app.py)                                                                   |
| **Home**                  | `/home`                           | Homepage with a welcome message                         | [`/api/app.py`](./api/app.py)                                                                   |
| **Get User**              | `/api/users/{field}`              | Get user(s) by ID, name, or list with pagination        | [`/api/routers/user_api.py`](./api/routers/user_api.py)                                         |
| **Register User**         | `/api/users/register`             | Register a new user with a unique username and email    | [`/api/routers/user_api.py`](./api/routers/user_api.py)                                         |
| **Login User**            | `/api/users/login`                | Login user by username/email and password               | [`/api/routers/user_api.py`](./api/routers/user_api.py)                                         |
| **Update User**           | `/api/users/{user_id}/update`     | Update user account details                             | [`/api/routers/user_api.py`](./api/routers/user_api.py)                                         |
| **Delete User**           | `/api/users/{user_id}/delete`     | Permanently delete a user account                       | [`/api/routers/user_api.py`](./api/routers/user_api.py)                                         |
| **Get Notes by Field**    | `/api/notes/{field}`              | Retrieve notes by field (title, content, list, or id)   | [`/api/routers/note_api.py`](./api/routers/note_api.py)                                         |
| **Create Note**           | `/api/notes/create`               | Create a new note                                       | [`/api/routers/note_api.py`](./api/routers/note_api.py)                                         |
| **Update Note**           | `/api/notes/{note_id}/update`     | Update an existing note by ID                           | [`/api/routers/note_api.py`](./api/routers/note_api.py)                                         |
| **Delete Note**           | `/api/notes/{note_id}/delete`     | Permanently delete a note by ID                         | [`/api/routers/note_api.py`](./api/routers/note_api.py)                                         |

---

**Note**: As additional routes are implemented, this README should be updated to reflect changes.