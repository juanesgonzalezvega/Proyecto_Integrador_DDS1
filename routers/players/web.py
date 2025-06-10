from fastapi import APIRouter, Request, Form, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
import operations.jugador_ops as jugador_ops
import operations.partido_ops as partido_ops
from models.jugador import JugadorConId
from models.partido import PartidoConId
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# ------------------ RUTAS DE BÚSQUEDA ------------------

@router.get("/players/search", response_class=HTMLResponse)
async def search_players(request: Request, id: Optional[int] = None, numero: Optional[int] = None):
    jugadores = jugador_ops.buscar_jugadores(id, numero)
    return templates.TemplateResponse("players/players_search_results.html", {
        "request": request,
        "jugadores": jugadores,
        "query": f"id={id} numero={numero}"
    })

@router.get("/games/search", response_class=HTMLResponse)
async def search_games(request: Request, id_partido: Optional[int] = None, rival: Optional[str] = None):
    partidos = partido_ops.buscar_partidos_por_oponente(id_partido, rival)
    return templates.TemplateResponse("players/games_search_results.html", {
        "request": request,
        "partidos": partidos,
        "query": f"id={id_partido} rival={rival}"
    })

# ------------------ RUTAS PARA CREAR JUGADOR ------------------

@router.get("/players/create", response_class=HTMLResponse)
async def create_player_form(request: Request):
    return templates.TemplateResponse("players/create.html", {"request": request})

@router.post("/players/create", response_class=HTMLResponse)
async def create_player(
    request: Request,
    nombre: str = Form(...),
    numero: int = Form(...),
    posicion: str = Form(...),
    equipo: str = Form(...),
    altura: float = Form(...),
    edad: int = Form(...)
):
    jugador = JugadorConId(
        id=0,
        nombre=nombre,
        numero=numero,
        posicion=posicion,
        equipo=equipo,
        altura=altura,
        edad=edad,
        estado="activo",
        eliminado="no"
    )
    nuevo_jugador = jugador_ops.agregar_jugador(jugador)
    return RedirectResponse(url=f"/players/{nuevo_jugador.id}", status_code=303)

# ------------------ RUTAS PARA CREAR PARTIDO ------------------

@router.get("/games/create", response_class=HTMLResponse)
async def create_game_form(request: Request):
    return templates.TemplateResponse("players/game_create.html", {"request": request})

@router.post("/games/create", response_class=HTMLResponse)
async def create_game(
    request: Request,
    fecha: str = Form(...),
    fase: str = Form(...),
    rival: str = Form(...),
    puntaje_usa: int = Form(...),
    puntaje_rival: int = Form(...),
    jugador_destacado: str = Form(...),
    puntos: int = Form(...),
    rebotes: int = Form(...),
    asistencias: int = Form(...),
    robos: int = Form(...),
    minutos_jugados: int = Form(...),
    estado: str = Form(...),
    eliminado: str = Form(...)
):
    partido = PartidoConId(
        id_partido=0,
        fecha=fecha,
        fase=fase,
        rival=rival,
        puntaje_usa=puntaje_usa,
        puntaje_rival=puntaje_rival,
        jugador_destacado=jugador_destacado,
        puntos=puntos,
        rebotes=rebotes,
        asistencias=asistencias,
        robos=robos,
        minutos_jugados=minutos_jugados,
        estado=estado,
        eliminado=eliminado
    )
    nuevo_partido = partido_ops.agregar_partido(partido)
    return RedirectResponse(url=f"/games/{nuevo_partido.id_partido}", status_code=303)

# ------------------ RUTAS DINÁMICAS PARA JUGADORES ------------------

@router.get("/players", response_class=HTMLResponse)
async def list_players(request: Request):
    jugadores = jugador_ops.leer_todos_los_jugadores()
    return templates.TemplateResponse("players/list.html", {"request": request, "jugadores": jugadores})

@router.get("/players/{id_jugador}", response_class=HTMLResponse)
async def player_detail(request: Request, id_jugador: int):
    jugador = jugador_ops.leer_un_jugador(id_jugador)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return templates.TemplateResponse("players/detail.html", {"request": request, "jugador": jugador})

@router.get("/players/{id_jugador}/edit", response_class=HTMLResponse)
async def edit_player_form(request: Request, id_jugador: int):
    jugador = jugador_ops.leer_un_jugador(id_jugador)
    if not jugador:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return templates.TemplateResponse("players/edit.html", {"request": request, "jugador": jugador})

@router.post("/players/{id_jugador}/edit", response_class=HTMLResponse)
async def edit_player(
    request: Request,
    id_jugador: int,
    nombre: str = Form(...),
    numero: int = Form(...),
    posicion: str = Form(...),
    equipo: str = Form(...),
    altura: float = Form(...),
    edad: int = Form(...),
    estado: str = Form(...),
    eliminado: str = Form(...)
):
    jugador = JugadorConId(
        id=id_jugador,
        nombre=nombre,
        numero=numero,
        posicion=posicion,
        equipo=equipo,
        altura=altura,
        edad=edad,
        estado=estado,
        eliminado=eliminado
    )
    modificado = jugador_ops.modificar_jugador(id_jugador, jugador)
    if not modificado:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return RedirectResponse(url=f"/players/{id_jugador}", status_code=303)

# ------------------ RUTAS DINÁMICAS PARA PARTIDOS ------------------

@router.get("/games", response_class=HTMLResponse)
async def list_games(request: Request):
    partidos = partido_ops.leer_todos_los_partidos()
    return templates.TemplateResponse("players/games_list.html", {"request": request, "partidos": partidos})

@router.get("/games/{id_partido}", response_class=HTMLResponse)
async def game_detail(request: Request, id_partido: int):
    partido = partido_ops.leer_un_partido(id_partido)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return templates.TemplateResponse("players/game_detail.html", {"request": request, "partido": partido})

@router.get("/games/{id_partido}/edit", response_class=HTMLResponse)
async def edit_game_form(request: Request, id_partido: int):
    partido = partido_ops.leer_un_partido(id_partido)
    if not partido:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return templates.TemplateResponse("players/game_edit.html", {"request": request, "partido": partido})

@router.post("/games/{id_partido}/edit", response_class=HTMLResponse)
async def edit_game(
    request: Request,
    id_partido: int,
    fecha: str = Form(...),
    fase: str = Form(...),
    rival: str = Form(...),
    puntaje_usa: int = Form(...),
    puntaje_rival: int = Form(...),
    jugador_destacado: str = Form(...),
    puntos: int = Form(...),
    rebotes: int = Form(...),
    asistencias: int = Form(...),
    robos: int = Form(...),
    minutos_jugados: int = Form(...),
    estado: str = Form(...),
    eliminado: str = Form(...)
):
    partido = PartidoConId(
        id_partido=id_partido,
        fecha=fecha,
        fase=fase,
        rival=rival,
        puntaje_usa=puntaje_usa,
        puntaje_rival=puntaje_rival,
        jugador_destacado=jugador_destacado,
        puntos=puntos,
        rebotes=rebotes,
        asistencias=asistencias,
        robos=robos,
        minutos_jugados=minutos_jugados,
        estado=estado,
        eliminado=eliminado
    )
    modificado = partido_ops.modificar_partido(id_partido, partido)
    if not modificado:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return RedirectResponse(url=f"/games/{id_partido}", status_code=303)

# ------------------ RUTA ABOUT ------------------

@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

# ------------------ RUTAS PARA ELIMINAR ------------------

@router.post("/players/{id_jugador}/delete")
async def delete_player(id_jugador: int):
    eliminado = jugador_ops.eliminar_jugador(id_jugador)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Jugador no encontrado")
    return RedirectResponse(url="/players", status_code=303)

@router.post("/games/{id_partido}/delete")
async def delete_game(id_partido: int):
    eliminado = partido_ops.eliminar_partido(id_partido)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return RedirectResponse(url="/games", status_code=303)