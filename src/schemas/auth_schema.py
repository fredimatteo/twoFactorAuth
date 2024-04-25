from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        from_attributes = True
