import os
from dotenv import load_dotenv
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()

DATABASE_URL = (
    f"postgresql+asyncpg://{os.getenv('POSTGRESQL_ADDON_USER')}:"
    f"{os.getenv('POSTGRESQL_ADDON_PASSWORD')}@"
    f"{os.getenv('POSTGRESQL_ADDON_HOST')}:"
    f"{os.getenv('POSTGRESQL_ADDON_PORT')}/"
    f"{os.getenv('POSTGRESQL_ADDON_DB')}"
)

async def test():
    engine = create_async_engine(DATABASE_URL, echo=True)
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1;")
        print("Conexión exitosa!")
    except Exception as e:
        print("Error de conexión:", e)

if __name__ == "__main__":
    asyncio.run(test())