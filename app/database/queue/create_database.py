from app.database.models.base import Base
from app.database.models.sync_engine import sync_engine


def create_database() -> None:
    with sync_engine.begin() as conn:
        conn.run_sync(Base.metadata.create_all)