from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    otp_validation_token: str

    class Config:
        from_attributes = True


class OtpRequest(BaseModel):
    otp_code: str
    validation_token: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        from_attributes = True
