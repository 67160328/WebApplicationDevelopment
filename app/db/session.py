from typing import Generator
from app.db.base import SessionLocal

def get_db() -> Generator:
    """Dependency that yields a database session and closes it afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
