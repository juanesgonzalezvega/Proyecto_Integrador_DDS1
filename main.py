import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db_connection import get_session, init_db
from sqlmodels_db import JugadorSQL, PartidoSQL
from operations.jugador_db_ops import (
    leer_todos_los_jugadores_db,
    leer_un_jugador_db,
    agregar_jugador_db,
    modificar_jugador_db,
    eliminar_jugador_db,
)
from operations.partido_db_ops import (
    leer_todos_los_partidos_db,
    leer_un_partido_db,
    agregar_partido_db,
    modificar_partido_db,
    eliminar_partido_db,
)

app = FastAPI(title="Proyecto Integrador DDS1")

@app.on_event("startup")
async def on_startup():
    await init_db()

# ---- Jugadores ----

@app.get("/jugadores")
async def get_jugadores(session: AsyncSession = Depends(get_session)):
    # Aquí usas la sesión correctamente
    jugadores = await leer_todos_los_jugadores_db(session)
    return jugadores

@app.get("/jugadores/{jugador_id}", response_model=JugadorSQL)
async def get_jugador(jugador_id: int, session: AsyncSession = Depends(get_session)):
    jugador = await leer_un_jugador_db(jugador_id, session)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

@app.post("/jugadores", response_model=JugadorSQL)
async def create_jugador(jugador: JugadorSQL, session: AsyncSession = Depends(get_session)):
    return await agregar_jugador_db(jugador, session)

@app.put("/jugadores/{jugador_id}", response_model=JugadorSQL)
async def update_jugador(jugador_id: int, jugador: JugadorSQL, session: AsyncSession = Depends(get_session)):
    data = jugador.dict(exclude_unset=True)
    updated = await modificar_jugador_db(jugador_id, data, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return updated

@app.delete("/jugadores/{jugador_id}", response_model=JugadorSQL)
async def delete_jugador(jugador_id: int, session: AsyncSession = Depends(get_session)):
    eliminado = await eliminar_jugador_db(jugador_id, session)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return eliminado

# ---- Partidos ----

@app.get("/partidos", response_model=List[PartidoSQL])
async def get_partidos(session: AsyncSession = Depends(get_session)):
    return await leer_todos_los_partidos_db(session)

@app.get("/partidos/{partido_id}", response_model=PartidoSQL)
async def get_partido(partido_id: int, session: AsyncSession = Depends(get_session)):
    partido = await leer_un_partido_db(partido_id, session)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido

@app.post("/partidos", response_model=PartidoSQL)
async def create_partido(partido: PartidoSQL, session: AsyncSession = Depends(get_session)):
    return await agregar_partido_db(partido, session)

@app.put("/partidos/{partido_id}", response_model=PartidoSQL)
async def update_partido(partido_id: int, partido: PartidoSQL, session: AsyncSession = Depends(get_session)):
    data = partido.dict(exclude_unset=True)
    updated = await modificar_partido_db(partido_id, data, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return updated

@app.delete("/partidos/{partido_id}", response_model=PartidoSQL)
async def delete_partido(partido_id: int, session: AsyncSession = Depends(get_session)):
    eliminado = await eliminar_partido_db(partido_id, session)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return eliminado

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)