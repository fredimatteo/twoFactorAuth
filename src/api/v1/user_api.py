from fastapi import APIRouter

from src.schemas import user_schema

router = APIRouter(prefix="/users", tags=["users"])


@router.get("")
def get_users():
    users = [
        user_schema.UserResponseSchema(
            id=1,
            first_name="Test",
            last_name="User",
            email="<EMAIL>",
        )
    ]

    return users
