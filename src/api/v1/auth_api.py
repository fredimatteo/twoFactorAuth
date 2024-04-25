from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas import auth_schema
from src.services.auth import generate_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", status_code=200, response_model=auth_schema.TokenResponse)
def create_token(src: auth_schema.LoginRequest, db: Session = Depends(get_db)):
    return generate_token(src, db)
