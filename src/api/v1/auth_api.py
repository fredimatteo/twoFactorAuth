import secrets

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.config.exception import NotFoundException, GenericException, InvalidCredentialsException
from src.schemas import auth_schema, user_schema
from src.services import user_service, otp_service
from src.services.auth_service import authenticate, generate_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    path="/verify-mail/{token}",
    status_code=status.HTTP_200_OK,
    response_model=user_schema.FirstLoginResponseSchema
)
def verify_mail(token: str, db: Session = Depends(get_db)):
    try:
        user = user_service.get_user_by_email_validation_token(db=db, validation_token=token)

        otp_secret: str = otp_service.generate_otp_secret()
        otp_qrcode: str = otp_service.generate_qr_code(otp_secret)

        user.disabled = False
        user.mail_validation_token = None
        user.otp_secret = otp_secret

        db.commit()
        return user_schema.FirstLoginResponseSchema(qrcode_otp=otp_qrcode, code_otp=otp_secret)
    except NotFoundException as e:
        raise NotFoundException(str(e)) from e
    except Exception as e:
        raise GenericException(str(e)) from e


@router.post("/login", status_code=status.HTTP_200_OK, response_model=auth_schema.LoginResponse)
def login(src: auth_schema.LoginRequest, db: Session = Depends(get_db)):
    try:
        user = authenticate(src.username, src.password, db)

        validation_token = secrets.token_urlsafe(42)
        user_service.update_user_otp_token(db=db, otp_validation_token=validation_token, user_id=user.id)

        db.commit()
        return auth_schema.LoginResponse(otp_validation_token=validation_token)
    except InvalidCredentialsException as e:
        raise InvalidCredentialsException(str(e)) from e
    except Exception as e:
        raise GenericException(str(e)) from e


@router.post("/otp/verify", status_code=status.HTTP_200_OK, response_model=auth_schema.TokenResponse)
def authenticate_by_otp(src: auth_schema.OtpRequest, db: Session = Depends(get_db)):
    try:
        user = otp_service.verify_otp(db=db, validation_token=src.validation_token, otp=src.otp_code)

        db.commit()
        return generate_token(src=user)
    except NotFoundException as e:
        raise NotFoundException(str(e)) from e
    except Exception as e:
        raise GenericException(str(e)) from e