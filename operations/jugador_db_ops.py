from typing import List, Optional
from sqlmodels_db import JugadorSQL
from db_connection import get_session
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

# Listar todos los jugadores
async def leer_todos_los_jugadores_db(session: AsyncSession) -> List[JugadorSQL]:
    result = await session.execute(select(JugadorSQL))
    return result.scalars().all()

# Leer un jugador por ID
async def leer_un_jugador_db(id_jugador: int, session: AsyncSession) -> Optional[JugadorSQL]:
    return await session.get(JugadorSQL, id_jugador)

# Agregar un jugador
async def agregar_jugador_db(jugador: JugadorSQL, session: AsyncSession) -> JugadorSQL:
    session.add(jugador)
    await session.commit()
    await session.refresh(jugador)
    return jugador

# Modificar un jugador
async def modificar_jugador_db(id_jugador: int, jugador_data: dict, session: AsyncSession) -> Optional[JugadorSQL]:
    jugador = await session.get(JugadorSQL, id_jugador)
    if not jugador:
        return None
    for key, value in jugador_data.items():
        setattr(jugador, key, value)
    await session.commit()
    await session.refresh(jugador)
    return jugador

# Eliminar (marcar eliminado) un jugador
async def eliminar_jugador_db(id_jugador: int, session: AsyncSession) -> Optional[JugadorSQL]:
    jugador = await session.get(JugadorSQL, id_jugador)
    if not jugador:
        return None
    jugador.eliminado = "si"
    await session.commit()
    await session.refresh(jugador)
    return jugador