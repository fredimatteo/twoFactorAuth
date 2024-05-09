import secrets

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.config import exception
from src.config.database import get_db
from src.schemas import auth_schema, user_schema
from src.services import user_service, otp_service
from src.services.auth_service import authenticate, generate_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/verify-mail/{token}", status_code=status.HTTP_200_OK, response_model=user_schema.FirstLoginResponseSchema)
def verify_mail(token: str, db: Session = Depends(get_db)):
    user = user_service.get_user_by_email_validation_token(db=db, validation_token=token)

    if not user:
        raise exception.BadRequestException("Invalid mail verification token")

    user.disabled = False
    user.mail_validation_token = None

    otp_secret = otp_service.generate_otp_secret()
    otp_qrcode = otp_service.generate_qr_code(otp_secret)

    user.otp_secret = otp_secret

    db.commit()

    return user_schema.FirstLoginResponseSchema(
        qrcode_otp=otp_qrcode,
        code_otp=otp_secret
    )


@router.post("/login", status_code=status.HTTP_200_OK, response_model=auth_schema.LoginResponse)
def login(src: auth_schema.LoginRequest, db: Session = Depends(get_db)):
    user = authenticate(src.username, src.password, db)

    validation_token = secrets.token_urlsafe(42)
    user_service.update_user_otp_token(db=db, otp_validation_token=validation_token, user_id=user.id)

    db.commit()

    return auth_schema.LoginResponse(otp_validation_token=validation_token)


@router.post("/otp/verify", status_code=status.HTTP_200_OK, response_model=auth_schema.TokenResponse)
def authenticate_by_otp(src: auth_schema.OtpRequest, db: Session = Depends(get_db)):
    user = otp_service.verify_otp(db=db, validation_token=src.validation_token, otp=src.otp_code)

    db.commit()

    if user:
        return generate_token(src=user)

    raise exception.BadRequestException("Invalid OTP")
