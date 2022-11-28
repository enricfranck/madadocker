from sqlalchemy.orm import Session

from db.base import Base
from crud import crud_users
from core import config
import schemas
from db.session import engine, SessionLocal

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28

Base.metadata.create_all(bind=engine)


def init_db() -> None:
    db: Session = SessionLocal()
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud_users.get_user_by_email(db, email=config.FIRST_SUPERUSER_MAIL)
    if not user:
        user_in = schemas.UserCreate(
            email=config.FIRST_SUPERUSER_MAIL,
            first_name=config.FIRST_SUPERUSER_MAIL,
            password=config.FIRST_SUPERUSER_PASSWORD,
            is_admin=True,
            is_superuser=True,
        )
        user = crud_users.create_user(db=db, user=user_in)  # noqa: F841
