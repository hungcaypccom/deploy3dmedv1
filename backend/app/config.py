from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

#config database: "postgresql+asyncpg://user:password@host:port/database"
DB_CONFIG = f"postgresql+asyncpg://postgres:1234567890@host.docker.internal:5432/test"


SECRET_KEY_ACCESS_TOKEN = "3DmedVN23"
SECRET_KEY_REFRESH_TOKEN = "3DmedVN23768686"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
ACCESS_TOKEN_EXPIRE_DAYS = 7
ACCESS_TOKEN_EXPIRE_YEARS = 1
REFRESH_TOKEN_EXPIRE_MINUTES = 10
REFRESH_TOKEN_EXPIRE_DAYS = 7
REFRESH_TOKEN_EXPIRE_YEARS = 1

#CHOICE: MINUTES, DAYS, YEARS, NONE = NEVER EXPIRE
ACCESS_TOKEN_EXPIRE_TYPE = "MINUTES"
REFRESH_TOKEN_EXPIRE_TYPE = "MINUTES"

class AsyncDatabaseSession:

    def __init__(self) -> None:
        self.session = None
        self.engine = None

    def __getattr__(self,name):
        return getattr(self.session,name)

    def init(self):
        self.engine = create_async_engine(DB_CONFIG,future=True, echo=False)
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)()

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)


db = AsyncDatabaseSession()

async def commit_rollback():
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    