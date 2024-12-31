from database.connection import Base, engine
from database.models import User

async def initialize():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)