from fastapi import Request, status
from fastapi.responses import JSONResponse


class NotFoundException(Exception):
    def __init__(self, item_reference: int | str):
        self.item_reference = item_reference


class InvalidCredentialsException(Exception):
    def __init__(self, credential_type: str):
        self.credential_type = credential_type


def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": f"Item '{exc.item_reference}' not found."}
    )


def invalid_credentials_exception_handler(request: Request, exc: InvalidCredentialsException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": f"Invalid {exc.credential_type}."},
    )
