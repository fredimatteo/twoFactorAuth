import secrets

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.schemas import auth_schema
from src.services import user_service, otp_service
from src.services.auth_service import authenticate, generate_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", status_code=200, response_model=auth_schema.LoginResponse)
def login(src: auth_schema.LoginRequest, db: Session = Depends(get_db)):
    user = authenticate(src.username, src.password, db)

    validation_token = secrets.token_urlsafe(42)
    user_service.update_user_otp_token(db=db, otp_validation_token=validation_token, user_id=user.id)

    db.commit()

    qr_code = otp_service.generate_qr_code(user.otp_secret)

    return auth_schema.LoginResponse(otp_token=validation_token, img=qr_code)


@router.post("/otp", status_code=200)
def authenticate_by_otp(src: auth_schema.OtpRequest, db: Session = Depends(get_db)):
    user = otp_service.verify_otp(db=db, validation_token=src.validation_token, otp=src.otp_code)

    db.commit()

    if user:
        return generate_token(db=db, src=user)

    raise HTTPException(status_code=400, detail="Invalid OTP")
