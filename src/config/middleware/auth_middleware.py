from fastapi import Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.config.database import SessionLocal
from src.config.exception import GenericException, InvalidCredentialsException
from src.services import auth_service

security = HTTPBearer()


async def authenticate(credential: HTTPAuthorizationCredentials = Security(security)):
    try:
        db = SessionLocal()
        user = auth_service.decode_token(credential.credentials, db)
        return user
    except InvalidCredentialsException as e:
        raise InvalidCredentialsException(e.credential_type) from e
    except Exception as e:
        raise GenericException(message=str(e)) from e
