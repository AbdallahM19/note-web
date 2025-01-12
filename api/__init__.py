"""__init__.py"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from api.app import router, templates
from api.routers.user_api import router as user_router
from api.routers.note_api import router as note_router
from api.database import create_database, create_tables, drop_db

app = FastAPI()

# Session middleware configuration
app.add_middleware(SessionMiddleware, secret_key="mysecretkey2024")

app.include_router(router)
app.include_router(user_router)
app.include_router(note_router)

app.mount("/static", StaticFiles(directory="static"), name="static")


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


# Error Handler
@app.exception_handler(HTTPException)
async def not_found_exception_handler(req: Request, exc: HTTPException):
    """called when an HTTPException is raised"""
    return templates.TemplateResponse(
        request=req,
        name="error_page.html",
        context={
            "error_code": exc.status_code,
            "error_message": exc.detail or "Something went wrong",
            "error_detail": "Please contact support if the issue persists."
        },
        status_code=exc.status_code
    )

# @app.exception_handler(500)
# async def internal_server_error_handler(req: Request, exc: HTTPException):
#     """Custom 500 error handler"""
#     return templates.TemplateResponse(
#         request=req,
#         name="error_page.html",
#         context={
#             "error_code": exc.status_code,
#             "error_message": "Internal Server Error",
#             "error_detail": exc.detail
#         }
#     )

# def logger(func):
#     """logger function"""
#     def wrapper(*args, **kwargs):
#         """wrapper for load data the current user"""
#     return wrapper(func)
