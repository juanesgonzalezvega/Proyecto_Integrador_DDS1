import csv
from typing import List, Optional
from models.jugador import JugadorConId

PLAYERS_CSV = 'players.csv'
JUGELIM_CSV = 'jugelim.csv'


def leer_todos_los_jugadores() -> List[JugadorConId]:
    jugadores = []
    try:
        with open(PLAYERS_CSV, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for row in lector:
                jugador = JugadorConId(
                    id=int(row['id']),
                    nombre=row['nombre'],
                    numero=int(row['numero']),
                    posicion=row['posicion'],
                    equipo=row['equipo'],
                    altura=float(row['altura']),
                    edad=int(row['edad']),
                    estado=row.get('estado', 'activo'),
                    eliminado=row.get('eliminado', 'no')
                )
                jugadores.append(jugador)
    except FileNotFoundError:
        raise FileNotFoundError("Archivo de jugadores no encontrado")
    except Exception as e:
        raise Exception(f"Error al leer jugadores: {e}")
    return jugadores


def leer_un_jugador(id_jugador: int) -> Optional[JugadorConId]:
    jugadores = leer_todos_los_jugadores()
    for jugador in jugadores:
        if jugador.id == id_jugador:
            return jugador
    return None


def buscar_jugadores(id: Optional[int] = None, numero: Optional[int] = None) -> List[JugadorConId]:
    jugadores = leer_todos_los_jugadores()
    resultados = []
    for jugador in jugadores:
        if (id is not None and jugador.id == id) or \
                (numero is not None and jugador.numero == numero):
            resultados.append(jugador)
    return resultados


def agregar_jugador(jugador: JugadorConId) -> JugadorConId:
    jugadores = leer_todos_los_jugadores()
    jugador.id = max([j.id for j in jugadores], default=0) + 1

    if not hasattr(jugador, 'estado') or jugador.estado is None:
        jugador.estado = 'activo'
    if not hasattr(jugador, 'eliminado') or jugador.eliminado is None:
        jugador.eliminado = 'no'

    jugadores.append(jugador)

    with open(PLAYERS_CSV, mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([
            jugador.id,
            jugador.nombre,
            jugador.numero,
            jugador.posicion,
            jugador.equipo,
            jugador.altura,
            jugador.edad,
            jugador.estado,
            jugador.eliminado
        ])

    return jugador


def modificar_estado_jugador(id_jugador: int, estado: str) -> Optional[JugadorConId]:
    jugadores = leer_todos_los_jugadores()
    for jugador in jugadores:
        if jugador.id == id_jugador:
            jugador.estado = estado

            with open(PLAYERS_CSV, mode='w', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(
                    ['id', 'nombre', 'numero', 'posicion', 'equipo', 'altura', 'edad', 'estado', 'eliminado'])
                for j in jugadores:
                    escritor.writerow([
                        j.id,
                        j.nombre,
                        j.numero,
                        j.posicion,
                        j.equipo,
                        j.altura,
                        j.edad,
                        j.estado,
                        j.eliminado
                    ])
            return jugador
    return None


def modificar_jugador(id_jugador: int, jugador: JugadorConId) -> Optional[JugadorConId]:
    jugadores = leer_todos_los_jugadores()
    for j in jugadores:
        if j.id == id_jugador:
            j.nombre = jugador.nombre
            j.numero = jugador.numero
            j.posicion = jugador.posicion
            j.equipo = jugador.equipo
            j.altura = jugador.altura
            j.edad = jugador.edad
            j.estado = jugador.estado
            j.eliminado = jugador.eliminado

            with open(PLAYERS_CSV, mode='w', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(
                    ['id', 'nombre', 'numero', 'posicion', 'equipo', 'altura', 'edad', 'estado', 'eliminado'])
                for jugador in jugadores:
                    escritor.writerow([
                        jugador.id,
                        jugador.nombre,
                        jugador.numero,
                        jugador.posicion,
                        jugador.equipo,
                        jugador.altura,
                        jugador.edad,
                        jugador.estado,
                        jugador.eliminado
                    ])
            return j
    return None


def eliminar_jugador(id_jugador: int) -> Optional[JugadorConId]:
    jugadores = leer_todos_los_jugadores()
    jugador_a_eliminar = None

    for jugador in jugadores:
        if jugador.id == id_jugador:
            jugador_a_eliminar = jugador
            jugador.eliminado = "si"
            break

    if jugador_a_eliminar:
        with open(JUGELIM_CSV, mode='a', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([
                jugador_a_eliminar.id,
                jugador_a_eliminar.nombre,
                jugador_a_eliminar.numero,
                jugador_a_eliminar.posicion,
                jugador_a_eliminar.equipo,
                jugador_a_eliminar.altura,
                jugador_a_eliminar.edad,
                jugador_a_eliminar.estado,
                jugador_a_eliminar.eliminado
            ])

        with open(PLAYERS_CSV, mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(['id', 'nombre', 'numero', 'posicion', 'equipo', 'altura', 'edad', 'estado', 'eliminado'])
            for jugador in jugadores:
                escritor.writerow([
                    jugador.id,
                    jugador.nombre,
                    jugador.numero,
                    jugador.posicion,
                    jugador.equipo,
                    jugador.altura,
                    jugador.edad,
                    jugador.estado,
                    jugador.eliminado
                ])

        return jugador_a_eliminar
    return None


def obtener_jugadores_eliminados() -> List[JugadorConId]:
    jugadores = leer_todos_los_jugadores()
    return [jugador for jugador in jugadores if jugador.eliminado == "si"]