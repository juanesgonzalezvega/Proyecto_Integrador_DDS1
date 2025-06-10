import csv
from typing import List, Optional
from models.partido import PartidoConId

GAMES_CSV = 'games.csv'
PARTELIM_CSV = 'partelim.csv'


def leer_todos_los_partidos() -> List[PartidoConId]:
    partidos = []
    try:
        with open(GAMES_CSV, mode='r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for row in lector:
                partido = PartidoConId(
                    id_partido=int(row['id_partido']),
                    fecha=row['fecha'],
                    fase=row['fase'],
                    rival=row['rival'],
                    puntaje_usa=int(row['puntaje_usa']),
                    puntaje_rival=int(row['puntaje_rival']),
                    jugador_destacado=row['jugador_destacado'],
                    puntos=int(row['puntos']),
                    rebotes=int(row['rebotes']),
                    asistencias=int(row['asistencias']),
                    robos=int(row['robos']),
                    minutos_jugados=int(row['minutos_jugados']),
                    estado=row.get('estado', 'jugado'),
                    eliminado=row.get('eliminado', 'no')
                )
                partidos.append(partido)
    except FileNotFoundError:
        raise FileNotFoundError("Archivo de partidos no encontrado")
    except Exception as e:
        raise Exception(f"Error al leer partidos: {e}")
    return partidos


def leer_un_partido(id_partido: int) -> Optional[PartidoConId]:
    partidos = leer_todos_los_partidos()
    for partido in partidos:
        if partido.id_partido == id_partido:
            return partido
    return None


def buscar_partidos_por_oponente(id_partido: Optional[int] = None, rival: Optional[str] = None) -> List[PartidoConId]:
    if id_partido is None and (rival is None or rival.strip() == ""):
        return []

    partidos = leer_todos_los_partidos()
    resultados = []

    for partido in partidos:
        if (id_partido is not None and partido.id_partido == id_partido) or \
           (rival is not None and rival.strip() != "" and rival.lower() in partido.rival.lower()):
            resultados.append(partido)

    return resultados


def agregar_partido(partido: PartidoConId) -> PartidoConId:
    partidos = leer_todos_los_partidos()
    partido.id_partido = max([p.id_partido for p in partidos], default=0) + 1
    if not hasattr(partido, 'estado') or partido.estado is None:
        partido.estado = 'jugado'
    if not hasattr(partido, 'eliminado') or partido.eliminado is None:
        partido.eliminado = 'no'
    partidos.append(partido)
    with open(GAMES_CSV, mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([
            partido.id_partido, partido.fecha, partido.fase, partido.rival,
            partido.puntaje_usa, partido.puntaje_rival, partido.jugador_destacado,
            partido.puntos, partido.rebotes, partido.asistencias,
            partido.robos, partido.minutos_jugados, partido.estado, partido.eliminado
        ])
    return partido


def modificar_estado_partido(id_partido: int, estado: str) -> Optional[PartidoConId]:
    partidos = leer_todos_los_partidos()
    for partido in partidos:
        if partido.id_partido == id_partido:
            partido.estado = estado
            with open(GAMES_CSV, mode='w', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow([
                    'id_partido', 'fecha', 'fase', 'rival',
                    'puntaje_usa', 'puntaje_rival', 'jugador_destacado',
                    'puntos', 'rebotes', 'asistencias', 'robos',
                    'minutos_jugados', 'estado', 'eliminado'
                ])
                for p in partidos:
                    escritor.writerow([
                        p.id_partido, p.fecha, p.fase, p.rival,
                        p.puntaje_usa, p.puntaje_rival, p.jugador_destacado,
                        p.puntos, p.rebotes, p.asistencias, p.robos,
                        p.minutos_jugados, p.estado, p.eliminado
                    ])
            return partido
    return None


def modificar_partido(id_partido: int, partido: PartidoConId) -> Optional[PartidoConId]:
    partidos = leer_todos_los_partidos()
    for p in partidos:
        if p.id_partido == id_partido:
            p.fecha = partido.fecha
            p.fase = partido.fase
            p.rival = partido.rival
            p.puntaje_usa = partido.puntaje_usa
            p.puntaje_rival = partido.puntaje_rival
            p.jugador_destacado = partido.jugador_destacado
            p.puntos = partido.puntos
            p.rebotes = partido.rebotes
            p.asistencias = partido.asistencias
            p.robos = partido.robos
            p.minutos_jugados = partido.minutos_jugados
            p.estado = partido.estado
            p.eliminado = partido.eliminado
            with open(GAMES_CSV, mode='w', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow([
                    'id_partido', 'fecha', 'fase', 'rival',
                    'puntaje_usa', 'puntaje_rival', 'jugador_destacado',
                    'puntos', 'rebotes', 'asistencias', 'robos',
                    'minutos_jugados', 'estado', 'eliminado'
                ])
                for partido in partidos:
                    escritor.writerow([
                        partido.id_partido, partido.fecha, partido.fase, partido.rival,
                        partido.puntaje_usa, partido.puntaje_rival, partido.jugador_destacado,
                        partido.puntos, partido.rebotes, partido.asistencias, partido.robos,
                        partido.minutos_jugados, partido.estado, partido.eliminado
                    ])
            return p
    return None


def eliminar_partido(id_partido: int) -> Optional[PartidoConId]:
    partidos = leer_todos_los_partidos()
    partido_a_eliminar = None
    for partido in partidos:
        if partido.id_partido == id_partido:
            partido_a_eliminar = partido
            partido.eliminado = "si"
            break
    if partido_a_eliminar:
        with open(PARTELIM_CSV, mode='a', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([
                partido_a_eliminar.id_partido, partido_a_eliminar.fecha, partido_a_eliminar.fase,
                partido_a_eliminar.rival, partido_a_eliminar.puntaje_usa, partido_a_eliminar.puntaje_rival,
                partido_a_eliminar.jugador_destacado, partido_a_eliminar.puntos, partido_a_eliminar.rebotes,
                partido_a_eliminar.asistencias, partido_a_eliminar.robos, partido_a_eliminar.minutos_jugados,
                partido_a_eliminar.estado, partido_a_eliminar.eliminado
            ])
        with open(GAMES_CSV, mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([
                'id_partido', 'fecha', 'fase', 'rival',
                'puntaje_usa', 'puntaje_rival', 'jugador_destacado',
                'puntos', 'rebotes', 'asistencias', 'robos',
                'minutos_jugados', 'estado', 'eliminado'
            ])
            for partido in partidos:
                escritor.writerow([
                    partido.id_partido, partido.fecha, partido.fase, partido.rival,
                    partido.puntaje_usa, partido.puntaje_rival, partido.jugador_destacado,
                    partido.puntos, partido.rebotes, partido.asistencias, partido.robos,
                    partido.minutos_jugados, partido.estado, partido.eliminado
                ])
        return partido_a_eliminar
    return None


def obtener_partidos_eliminados() -> List[PartidoConId]:
    partidos = leer_todos_los_partidos()
    return [partido for partido in partidos if partido.eliminado == "si"]
