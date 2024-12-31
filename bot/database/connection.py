from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from config import DB_PATH

engine = create_async_engine(f"sqlite+aiosqlite:///{DB_PATH}",echo=False)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession)

Base = declarative_base()