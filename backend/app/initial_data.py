#!/usr/bin/env python3

from crud.crud_users import create_user
from db.init_db import init_db
from schemas.schemas import UserCreate
from db.session import SessionLocal


def init() -> None:
    db = SessionLocal()
    init_db(db)

    create_user(
        db,
        UserCreate(
            email="admin@test.com",
            password="admin",
            is_active=True,
            is_superuser=True,
        ),
    )


if __name__ == "__main__":
    print("Creating superuser admin@test.com")
    init()
    print("Superuser created")
