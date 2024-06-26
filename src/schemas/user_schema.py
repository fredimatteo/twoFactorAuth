from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int | None = None
    first_name: str
    last_name: str
    email: str
    password: str
    salt: str

    class Config:
        from_attributes = True


class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    username: str
    is_admin: bool
    disabled: bool

    class Config:
        from_attributes = True


class UserCreateSchema(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    username: str

    class Config:
        from_attributes = True


class FirstLoginResponseSchema(BaseModel):
    qrcode_otp: str
    code_otp: str

    class Config:
        from_attributes = True


class VerifyEmailResponseSchema(BaseModel):
    email: str
    token: str

    class Config:
        from_attributes = True
