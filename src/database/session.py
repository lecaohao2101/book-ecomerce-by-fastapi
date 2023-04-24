from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool


SQLALCHEMY_DATABASE_URI = 'sqlite:///src/app.db'

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}, poolclass=QueuePool, max_overflow=100, pool_size=60)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()