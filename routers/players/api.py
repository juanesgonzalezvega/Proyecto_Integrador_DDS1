from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Optional

from models.jugador import JugadorConId
from models.partido import PartidoConId
import operations.jugador_ops as jugador_ops
import operations.partido_ops as partido_ops

router = APIRouter()

# ----------------------------
# Endpoints de Jugadores
# ----------------------------

@router.get("/players", response_model=List[JugadorConId])
async def obtener_todos_los_jugadores():
    jugadores = jugador_ops.leer_todos_los_jugadores()
    jugadores_activos = [j for j in jugadores if j.estado == "activo"]
    if not jugadores_activos:
        raise HTTPException(status_code=404, detail="No se encontraron jugadores activos")
    return jugadores_activos

@router.get("/players/{id_jugador}", response_model=JugadorConId)
async def obtener_jugador(id_jugador: int):
    jugador = jugador_ops.leer_un_jugador(id_jugador)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

@router.get("/players/search", response_model=List[JugadorConId])
async def buscar_jugador(
    numero_camiseta: Optional[int] = Query(None),
    apellido: Optional[str] = Query(None)
):
    jugadores = jugador_ops.buscar_jugadores(numero_camiseta, apellido)
    if not jugadores:
        raise HTTPException(status_code=404, detail="No se encontraron jugadores")
    return jugadores

@router.post("/players", response_model=JugadorConId)
async def agregar_jugador(jugador: JugadorConId):
    nuevo_jugador = jugador_ops.agregar_jugador(jugador)
    return nuevo_jugador

@router.put("/players/{id_jugador}/status", response_model=JugadorConId)
async def modificar_estado_jugador_endpoint(
    id_jugador: int,
    estado: str = Body(..., embed=True)
):
    jugador_modificado = jugador_ops.modificar_estado_jugador(id_jugador, estado)
    if jugador_modificado is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador_modificado

@router.put("/players/{id_jugador}", response_model=JugadorConId)
async def modificar_jugador_endpoint(id_jugador: int, jugador: JugadorConId):
    jugador_modificado = jugador_ops.modificar_jugador(id_jugador, jugador)
    if jugador_modificado is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador_modificado

@router.delete("/players/{id_jugador}", response_model=JugadorConId)
async def eliminar_jugador_endpoint(id_jugador: int):
    jugador_eliminado = jugador_ops.eliminar_jugador(id_jugador)
    if jugador_eliminado is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador_eliminado

@router.get("/players/deleted", response_model=List[JugadorConId])
async def obtener_jugadores_eliminados():
    jugadores_eliminados = jugador_ops.obtener_jugadores_eliminados()
    if not jugadores_eliminados:
        raise HTTPException(status_code=404, detail="No se encontraron jugadores eliminados")
    return jugadores_eliminados

# ----------------------------
# Endpoints de Partidos
# ----------------------------

@router.get("/games", response_model=List[PartidoConId])
async def obtener_todos_los_partidos():
    partidos = partido_ops.leer_todos_los_partidos()
    if not partidos:
        raise HTTPException(status_code=404, detail="No se encontraron partidos")
    return partidos

@router.get("/games/{id_partido}", response_model=PartidoConId)
async def obtener_partido(id_partido: int):
    partido = partido_ops.leer_un_partido(id_partido)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido

@router.get("/games/search", response_model=List[PartidoConId])
async def buscar_partido(oponente: Optional[str] = Query(None)):
    partidos = partido_ops.buscar_partidos_por_oponente(oponente)
    if not partidos:
        raise HTTPException(status_code=404, detail="No se encontraron partidos")
    return partidos

@router.post("/games", response_model=PartidoConId)
async def agregar_partido(partido: PartidoConId):
    nuevo_partido = partido_ops.agregar_partido(partido)
    return nuevo_partido

@router.put("/games/{id_partido}/status", response_model=PartidoConId)
async def modificar_estado_partido_endpoint(
    id_partido: int,
    estado: str = Body(..., embed=True)
):
    partido_modificado = partido_ops.modificar_estado_partido(id_partido, estado)
    if partido_modificado is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido_modificado

@router.put("/games/{id_partido}", response_model=PartidoConId)
async def modificar_partido_endpoint(id_partido: int, partido: PartidoConId):
    partido_modificado = partido_ops.modificar_partido(id_partido, partido)
    if partido_modificado is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido_modificado

@router.delete("/games/{id_partido}", response_model=PartidoConId)
async def eliminar_partido_endpoint(id_partido: int):
    partido_eliminado = partido_ops.eliminar_partido(id_partido)
    if partido_eliminado is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido_eliminado

@router.get("/games/deleted", response_model=List[PartidoConId])
async def obtener_partidos_eliminados():
    partidos_eliminados = partido_ops.obtener_partidos_eliminados()
    if not partidos_eliminados:
        raise HTTPException(status_code=404, detail="No se encontraron partidos eliminados")
    return partidos_eliminados
