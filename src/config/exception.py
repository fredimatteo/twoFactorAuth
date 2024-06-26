import logging

from fastapi import Request, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class NotFoundException(Exception):
    def __init__(self, item_reference: int | str | None = None):
        if item_reference is None:
            self.message = "Item not found"
        else:
            self.message = f"Item {item_reference} not found"


class InvalidCredentialsException(Exception):
    def __init__(self, credential_type: str):
        self.credential_type = credential_type


class GenericException(Exception):
    def __init__(self, message: str):
        self.message = message


class BadRequestException(Exception):
    def __init__(self, message: str):
        self.message = message


# pylint: disable=unused-argument
def not_found_exception_handler(request: Request, exc: NotFoundException):
    logger.error(exc.message)
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message}
    )


# pylint: disable=unused-argument
def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": f"Invalid {exc.credential_type}."},
    )


# pylint: disable=unused-argument
def generic_exception_handler(request: Request, exc: GenericException):
    logger.error("an error occurred: %s", exc.message)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "An unknown error occurred."}
    )


# pylint: disable=unused-argument
def bad_request_exception_handler(request: Request, exc: BadRequestException):
    logger.error("an error occurred: %s", exc.message)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": exc.message}
    )
