from pydantic import BaseModel

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