import datetime
from pydantic import ConfigDict
from sqlmodel import SQLModel, Field
from typing import Optional


class JugadorBase(SQLModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    numero: int = Field(..., ge=0)
    posicion: str = Field(..., min_length=1, max_length=50)
    equipo: str = Field(..., min_length=1, max_length=100)
    altura: float = Field(..., ge=0)
    edad: int = Field(..., ge=0)
    estado: str = Field(..., min_length=1, max_length=20)
    eliminado: str = Field(..., min_length=1, max_length=5)


class JugadorSQL(JugadorBase, table=True):
    __tablename__ = "jugadores"
    id: Optional[int] = Field(default=None, primary_key=True)
    model_config = ConfigDict(from_attributes=True)


class PartidoBase(SQLModel):
    fecha: str = Field(..., min_length=1, max_length=20)
    fase: str = Field(..., min_length=1, max_length=50)
    rival: str = Field(..., min_length=1, max_length=100)
    puntaje_usa: int = Field(..., ge=0)
    puntaje_rival: int = Field(..., ge=0)
    jugador_destacado: str = Field(..., min_length=1, max_length=100)
    puntos: int = Field(..., ge=0)
    rebotes: int = Field(..., ge=0)
    asistencias: int = Field(..., ge=0)
    robos: int = Field(..., ge=0)
    minutos_jugados: int = Field(..., ge=0)
    estado: str = Field(..., min_length=1, max_length=20)
    eliminado: str = Field(..., min_length=1, max_length=5)


class PartidoSQL(PartidoBase, table=True):
    __tablename__ = "partidos"
    id_partido: Optional[int] = Field(default=None, primary_key=True)
    model_config = ConfigDict(from_attributes=True)
