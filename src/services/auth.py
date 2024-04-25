from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.config import settings
from src.models import user_model
from src.schemas.auth_schema import LoginRequest, TokenResponse
from src.services import user as user_service

st = settings.get_settings()

# openssl rand -hex 32
ALGORITHM = "HS256"
SECRET_KEY = st.jwt_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def __authenticate(username: str, password: str, db: Session) -> user_model.User:
    statement = select(user_model.User).where(user_model.User.username == username)

    result: user_model.User = db.execute(statement).scalar()

    if not result:
        raise HTTPException(status_code=404, detail="Invalid username")

    if not verify_password(password, result.password, result.salt):
        raise HTTPException(status_code=401, detail="Invalid password")

    return result


def generate_token(src: LoginRequest, db: Session) -> TokenResponse:
    user = __authenticate(src.username, src.password, db)
    if user:
        access_token = create_access_token(
            {
                "sub": user.username,
                "is_admin": user.is_admin,
            }
        )

        return TokenResponse(access_token=access_token, refresh_token="None", token_type="Bearer")

    raise HTTPException(status_code=401, detail="Incorrect username")


def decode_token(token: str, db: Session) -> user_model.User:
    CREDENTIALS_EXCEPTION = HTTPException(
                status_code=401,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise CREDENTIALS_EXCEPTION
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    user = user_service.get_user_by_username(db, username)
    if user is None:
        raise CREDENTIALS_EXCEPTION
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
