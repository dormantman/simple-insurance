from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from services.api import router as api_router
from core.config import ALLOWED_HOSTS, API_PREFIX, DEBUG, PROJECT_NAME, VERSION, WEB_PREFIX
from errors import http422_error_handler, http_error_handler
from core.events import create_start_app_handler, create_stop_app_handler
from services.web import router as web_router


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)

    application.mount("/static", StaticFiles(directory="static"), name="static")

    application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_stop_app_handler(application))

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router, prefix=API_PREFIX)
    application.include_router(web_router, prefix=WEB_PREFIX)

    return application


app = get_application()
