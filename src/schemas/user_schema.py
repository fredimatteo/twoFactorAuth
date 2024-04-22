from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int | None = None
    first_name: str
    last_name: str
    email: str
    password: str
    salt: str

    class Config:
        orm_mode = True


