from fastapi import Request, status
from fastapi.responses import JSONResponse


class NotFoundException(Exception):
    def __init__(self, item_reference: int | str | None = None):
        if item_reference is None:
            self.message = "Item not found"
        else:
            self.message = f"Item {item_reference} not found"


class InvalidCredentialsException(Exception):
    def __init__(self, credential_type: str):
        self.credential_type = credential_type


# pylint: disable=unused-argument
def not_found_exception_handler(request: Request, exc: NotFoundException):
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
