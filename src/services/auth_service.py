import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.config import settings, exception
from src.models import user_model
from src.schemas.auth_schema import TokenResponse
from src.services import user_service

st = settings.get_settings()

# openssl rand -hex 32
ALGORITHM = "HS256"
SECRET_KEY = st.jwt_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def authenticate(username: str, password: str, db: Session) -> user_model.User:
    try:
        statement = select(user_model.User).where(user_model.User.username == username)

        result: user_model.User = db.execute(statement).scalar()

        if not result:
            raise exception.InvalidCredentialsException("username")

        if not verify_password(password, result.password, result.salt):
            raise exception.InvalidCredentialsException("password")

        if result.disabled:
            raise exception.InvalidCredentialsException("disabled")

        return result
    except exception.InvalidCredentialsException as e:
        raise exception.InvalidCredentialsException(e.credential_type) from e
    except Exception as e:
        raise exception.GenericException(message=str(e))


def generate_token(src: user_model.User) -> TokenResponse:
    access_token = create_access_token(
        {
            "sub": src.username,
            "is_admin": src.is_admin,
        }
    )

    return TokenResponse(access_token=access_token, refresh_token="None", token_type="Bearer")


def decode_token(token: str, db: Session) -> user_model.User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise exception.InvalidCredentialsException("username")
    except JWTError:
        raise exception.InvalidCredentialsException("username")
    user = user_service.get_user_by_username(db, username)
    if user is None:
        raise exception.InvalidCredentialsException("username")
    return user


def hash_password(password: str, salt: str) -> str:
    return pwd_context.hash(password + salt)


def verify_password(plain_password: str, hashed_password: str, salt: str) -> bool:
    return pwd_context.verify(plain_password + salt, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def generate_temporary_token():
    random_value = secrets.token_urlsafe(16)

    timestamp = str(datetime.now(timezone.utc) + timedelta(minutes=15))

    token_data = random_value + timestamp

    hash_object = hashlib.sha256(token_data.encode())
    token_hash = hash_object.hexdigest()

    return token_hash
