from http import HTTPStatus
from fastapi import APIRouter, HTTPException
from app.database import users
from app.models.User import User, UserCreate, UserUpdate

from fastapi_pagination import Page
from app.database.users import get_users_paginated

router = APIRouter(prefix="/api/users")


@router.get("/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int) -> User:
    """Endpoint. Get user by user_id"""
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    user = users.get_user(user_id)

    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")
    return user


@router.get('/', status_code=HTTPStatus.OK)
def get_users() -> Page[User]:
    """Endpoint. Get all users"""
    return get_users_paginated()


@router.post("/", status_code=HTTPStatus.CREATED)
def create_user(user: User) -> User:
    """Endpoint. Create new user"""
    UserCreate.model_validate(user.model_dump())
    return users.create_user(user)


@router.patch("/{user_id}", status_code=HTTPStatus.OK)
def update_user(user_id: int, user: User) -> User:
    """Endpoint. Update user by user_id"""
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    UserUpdate.model_validate(user.model_dump())
    return users.update_user(user_id, user)


@router.delete("/{user_id}", status_code=HTTPStatus.OK)
def delete_user(user_id: int):
    """Endpoint. Delete user by user_id"""
    if user_id < 1:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Invalid user id")
    users.delete_user(user_id)
    return {"message": "User deleted"}
