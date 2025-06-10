from typing import List, Optional
from sqlmodels_db import PartidoSQL
from db_connection import get_session
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

# Listar todos los partidos
async def leer_todos_los_partidos_db(session: AsyncSession) -> List[PartidoSQL]:
    result = await session.execute(select(PartidoSQL))
    return result.scalars().all()

# Leer un partido por ID
async def leer_un_partido_db(id_partido: int, session: AsyncSession) -> Optional[PartidoSQL]:
    return await session.get(PartidoSQL, id_partido)

# Agregar un partido
async def agregar_partido_db(partido: PartidoSQL, session: AsyncSession) -> PartidoSQL:
    session.add(partido)
    await session.commit()
    await session.refresh(partido)
    return partido

# Modificar un partido
async def modificar_partido_db(id_partido: int, partido_data: dict, session: AsyncSession) -> Optional[PartidoSQL]:
    partido = await session.get(PartidoSQL, id_partido)
    if not partido:
        return None
    for key, value in partido_data.items():
        setattr(partido, key, value)
    await session.commit()
    await session.refresh(partido)
    return partido

# Eliminar (marcar eliminado) un partido
async def eliminar_partido_db(id_partido: int, session: AsyncSession) -> Optional[PartidoSQL]:
    partido = await session.get(PartidoSQL, id_partido)
    if not partido:
        return None
    partido.eliminado = "si"
    await session.commit()
    await session.refresh(partido)
    return partido