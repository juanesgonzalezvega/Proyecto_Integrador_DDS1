from pydantic import BaseModel

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
