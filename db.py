from sqlalchemy import create_engine
from sqlmodel import Session

engine = create_engine(
    "sqlite:///carsharing.db",
    connect_args={"check_same_thread": False},  # Needed for sqlite to run sql commands asynchronously
    echo=True  # For logging the sql commands
)


def get_session():
    with Session(engine) as session:
        yield session
