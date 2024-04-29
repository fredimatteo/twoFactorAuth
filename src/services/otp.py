import base64
from io import BytesIO

import pyotp
import qrcode
from sqlalchemy.orm import Session

from src.models import user_model
from src.services import user as user_service


def generate_qr_code(secret):
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(issuer_name="JWT-APP")
    img = qrcode.make(uri)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_str


def generate_otp_secret() -> str:
    return pyotp.random_base32()


def verify_otp(otp: str, validation_token: str, db: Session) -> user_model.User | None:
    user = user_service.get_user_by_otp_validation_token(db=db, validation_token=validation_token)

    totp = pyotp.TOTP(user.otp_secret)
    if totp.verify(otp):
        user_service.update_user_otp_token(db=db, otp_validation_token=None, user_id=user.id)

        return user

    return None
