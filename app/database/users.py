from http.client import HTTPException
from typing import Iterable

from sqlmodel import Session, select
from app.database.engine import engine
from app.models.User import User

from fastapi_pagination import Page
from fastapi_pagination.ext.sqlmodel import paginate


def get_user(user_id: int) -> User | None:
    """Get user by id"""
    with Session(engine) as session:
        return session.get(User, user_id)


def get_users() -> Iterable[User]:
    """Get all users"""
    with Session(engine) as session:
        statement = select(User)
        return session.exec(statement).all()


def get_users_paginated() -> Page[User]:
    """Get all users paginated"""
    with Session(engine) as session:
        return paginate(session, select(User))


def create_user(user: User) -> User:
    """Create new user"""
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def update_user(user_id: int, user: User) -> User:
    """Update user by id"""
    with Session(engine) as session:
        db_user = session.get(User, user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="bd user not found")
        user_data = user.model_dump(exclude_unset=True)
        db_user.sqlmodel_update(user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user


def delete_user(user_id: int):
    """Delete user by id"""
    with Session(engine) as session:
        user = session.get(User, user_id)
        session.delete(user)
        session.commit()
