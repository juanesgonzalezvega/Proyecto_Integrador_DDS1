from pydantic import BaseModel
from typing import Optional

class JugadorConId(BaseModel):
    id: int
    nombre: str
    numero: int
    posicion: str
    equipo: str
    altura: float
    edad: int
    estado: str
    eliminado: str

class PartidoConId(BaseModel):
    id_partido: int
    fecha: str
    fase: str
    rival: str
    puntaje_usa: int
    puntaje_rival: int
    jugador_destacado: str
    puntos: int
    rebotes: int
    asistencias: int
    robos: int
    minutos_jugados: int
    estado: str
    eliminado: str