from fastapi import status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder

from starlette.responses import RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from authlib.integrations.starlette_client import OAuthError

from payloads.responses import ErrorResponse, ValidationErrorResponse

def http_exception_handler(request: Request, exception: StarletteHTTPException):
    return JSONResponse(status_code=exception.status_code, content=ErrorResponse(error=exception.detail).model_dump())

def request_validation_error_handler(request: Request, exception: RequestValidationError):
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=jsonable_encoder(ValidationErrorResponse(error="The request data was not valid. Please try again later, and if the issue persists, open an issue on GitHub.", context=exception.errors()).model_dump()))

def unhandled_exception_handler(request: Request, exception: Exception):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=ErrorResponse(error="Please try again later. If the issue persists, open an issue on GitHub.").model_dump())

def oauth_error_handler(request: Request, exception: OAuthError):
    return RedirectResponse(url='/', status_code=status.HTTP_303_SEE_OTHER)