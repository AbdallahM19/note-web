"""__init__.py"""

from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from api.app import router
from api.routers.user_api import router as user_router
from api.routers.note_api import router as note_router
from api.database import create_database, create_tables, drop_db

app = FastAPI()

# Session middleware configuration
app.add_middleware(SessionMiddleware, secret_key="mysecretkey2024")

app.include_router(router)
app.include_router(user_router)
app.include_router(note_router)


@app.on_event("startup")
async def before_first_request():
    """This function is called when the application is Starting down"""
    print("Starting app")
    create_database()
    create_tables()
    print("Application startup complete")

@app.on_event("shutdown")
async def before_close_app():
    """This function is called when the application is shutting down"""
    print("Closing app")
    # drop_db()
    print("Application shutdown complete")


# def logger(func):
#     """logger function"""
#     def wrapper(*args, **kwargs):
#         """wrapper for load data the current user"""
#     return wrapper(func)
