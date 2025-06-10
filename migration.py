import asyncio
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from typing import Type
import pandas as pd

# Carga variables de entorno
load_dotenv()

# Configuración de la base de datos desde variables de entorno
POSTGRESQL_ADDON_USER = os.getenv('POSTGRESQL_ADDON_USER')
POSTGRESQL_ADDON_PASSWORD = os.getenv('POSTGRESQL_ADDON_PASSWORD')
POSTGRESQL_ADDON_HOST = os.getenv('POSTGRESQL_ADDON_HOST')
POSTGRESQL_ADDON_PORT = os.getenv('POSTGRESQL_ADDON_PORT')
POSTGRESQL_ADDON_DB = os.getenv('POSTGRESQL_ADDON_DB')

if not all([
    POSTGRESQL_ADDON_USER,
    POSTGRESQL_ADDON_PASSWORD,
    POSTGRESQL_ADDON_HOST,
    POSTGRESQL_ADDON_PORT,
    POSTGRESQL_ADDON_DB
]):
    raise ValueError("Faltan variables de entorno para la conexión a la base de datos.")

DATABASE_URL = (
    f"postgresql+asyncpg://{POSTGRESQL_ADDON_USER}:"
    f"{POSTGRESQL_ADDON_PASSWORD}@"
    f"{POSTGRESQL_ADDON_HOST}:"
    f"{POSTGRESQL_ADDON_PORT}/"
    f"{POSTGRESQL_ADDON_DB}"
)

# Crear motor asíncrono
engine = create_async_engine(DATABASE_URL, echo=True)

# Importa tus modelos SQLModel
from sqlmodels_db import JugadorSQL, PartidoSQL  # Ajusta según tu estructura

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("Tablas creadas correctamente.")

async def import_csv_to_db(file_path: str, model: Type[SQLModel], session: AsyncSession):
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Archivo {file_path} no encontrado.")
        return
    except Exception as e:
        print(f"Error al leer {file_path}: {e}")
        return

    # Normalizar nombres de columnas
    df.columns = [col.strip() for col in df.columns]

    for _, row in df.iterrows():
        data = row.to_dict()
        data = {k: (None if pd.isna(v) else v) for k, v in data.items()}
        obj = model(**data)
        session.add(obj)

    await session.commit()
    print(f"Datos importados desde {file_path} a la tabla {model.__tablename__}.")

async def main():
    await create_db_and_tables()
    async with AsyncSession(engine) as session:
        await import_csv_to_db("players.csv", JugadorSQL, session)
        await import_csv_to_db("games.csv", PartidoSQL, session)

if __name__ == "__main__":
    asyncio.run(main())
