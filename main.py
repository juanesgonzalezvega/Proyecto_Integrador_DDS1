from fastapi import FastAPI, HTTPException, Query, Body
from starlette.responses import JSONResponse
from models import JugadorConId, PartidoConId
from operations import (
    leer_todos_los_jugadores,
    leer_un_jugador,
    buscar_jugadores,
    leer_todos_los_partidos,
    leer_un_partido,
    buscar_partidos_por_oponente,
    eliminar_jugador,
    eliminar_partido,
    modificar_estado_jugador,
    modificar_estado_partido,
    agregar_jugador,
    agregar_partido,
    obtener_jugadores_eliminados,
    obtener_partidos_eliminados,
    modificar_partido,
    modificar_jugador,
)
from typing import List, Optional

app = FastAPI()

# Obtener todos los jugadores activos
@app.get("/allplayers", response_model=List[JugadorConId])
async def obtener_todos_jugadores():
    jugadores = leer_todos_los_jugadores()
    jugadores_activos = [jugador for jugador in jugadores if jugador.estado == "activo"]
    if not jugadores_activos:
        raise HTTPException(status_code=404, detail="No se encontraron jugadores activos")
    return jugadores_activos

# Obtener un jugador por ID
@app.get("/player/{id_jugador}", response_model=JugadorConId)
async def obtener_jugador(id_jugador: int):
    jugador = leer_un_jugador(id_jugador)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador

# Buscar jugadores por número de camiseta o apellido
@app.get("/players/search", response_model=List[JugadorConId])
async def buscar_jugador(
    numero_camiseta: Optional[int] = Query(None),
    apellido: Optional[str] = Query(None)
):
    jugadores = buscar_jugadores(numero_camiseta, apellido)
    if not jugadores:
        raise HTTPException(status_code=404, detail="No se encontraron jugadores")
    return jugadores

# Modificar el estado de un jugador
@app.put("/player/{id_jugador}/status", response_model=JugadorConId)
async def modificar_estado_jugador_endpoint(
    id_jugador: int,
    estado: str = Body(..., embed=True)  # Corregido para recibir el estado del cuerpo
):
    jugador_modificado = modificar_estado_jugador(id_jugador, estado)
    if jugador_modificado is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador_modificado

# Agregar un nuevo jugador
@app.post("/player", response_model=JugadorConId)
async def agregar_jugador_endpoint(jugador: JugadorConId):
    nuevo_jugador = agregar_jugador(jugador)
    return nuevo_jugador

# Obtener todos los partidos
@app.get("/allgames", response_model=List[PartidoConId])
async def obtener_todos_los_partidos():
    partidos = leer_todos_los_partidos()
    if not partidos:
        raise HTTPException(status_code=404, detail="No se encontraron partidos")
    return partidos

# Obtener detalles de un partido por ID
@app.get("/game/{id_partido}", response_model=PartidoConId)
async def obtener_partido(id_partido: int):
    partido = leer_un_partido(id_partido)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido

# Buscar partidos por nombre del oponente
@app.get("/games/search", response_model=List[PartidoConId])
async def buscar_partido(oponente: Optional[str] = Query(None)):
    partidos = buscar_partidos_por_oponente(oponente)
    if not partidos:
        raise HTTPException(status_code=404, detail="No se encontraron partidos")
    return partidos

# Modificar el estado de un partido
@app.put("/game/{id_partido}/status", response_model=PartidoConId)
async def modificar_estado_partido_endpoint(
    id_partido: int,
    estado: str = Body(..., embed=True)  # Corregido para recibir el estado del cuerpo
):
    partido_modificado = modificar_estado_partido(id_partido, estado)
    if partido_modificado is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido_modificado

# Agregar un nuevo partido
@app.post("/game", response_model=PartidoConId)
async def agregar_partido_endpoint(partido: PartidoConId):
    nuevo_partido = agregar_partido(partido)
    return nuevo_partido


# Eliminar un jugador por ID
@app.delete("/player/{id_jugador}", response_model=JugadorConId)
async def eliminar_jugador_endpoint(id_jugador: int):
    jugador_eliminado = eliminar_jugador(id_jugador)
    if jugador_eliminado is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador_eliminado


# Eliminar un partido por ID
@app.delete("/game/{id_partido}", response_model=PartidoConId)
async def eliminar_partido_endpoint(id_partido: int):
    partido_eliminado = eliminar_partido(id_partido)
    if partido_eliminado is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido_eliminado

# Obtener jugadores eliminados
@app.get("/deletedplayers", response_model=List[JugadorConId])
async def obtener_jugadores_eliminados_endpoint():
    jugadores_eliminados = obtener_jugadores_eliminados()
    if not jugadores_eliminados:
        raise HTTPException(status_code=404, detail="No se encontraron jugadores eliminados")
    return jugadores_eliminados

# Obtener partidos eliminados
@app.get("/deletedgames", response_model=List[PartidoConId])
async def obtener_partidos_eliminados_endpoint():
    partidos_eliminados = obtener_partidos_eliminados()
    if not partidos_eliminados:
        raise HTTPException(status_code=404, detail="No se encontraron partidos eliminados")
    return partidos_eliminados

# Modificar información de un jugador
@app.put("/player/{id_jugador}", response_model=JugadorConId)
async def modificar_jugador_endpoint(id_jugador: int, jugador: JugadorConId):
    jugador_modificado = modificar_jugador(id_jugador, jugador)
    if jugador_modificado is None:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return jugador_modificado

# Modificar información de un partido
@app.put("/game/{id_partido}", response_model=PartidoConId)
async def modificar_partido_endpoint(id_partido: int, partido: PartidoConId):
    partido_modificado = modificar_partido(id_partido, partido)
    if partido_modificado is None:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return partido_modificado

# Página principal
@app.get("/")
async def root():
    return {"mensaje": "¡Bienvenido al sistema del Team USA!"}

# Manejo de errores
@app.exception_handler(HTTPException)
async def manejar_excepciones_http(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "mensaje": "Error en la solicitud",
            "detalle": exc.detail,
            "ruta": request.url.path
        },
    )