import csv
from typing import List, Optional
from models import JugadorConId, PartidoConId

# Leer todos los jugadores desde el archivo CSV
def leer_todos_los_jugadores() -> List[JugadorConId]:
    jugadores = []
    try:
        with open('players.csv', mode='r', encoding='utf-8') as archivo:
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
                    estado=row.get('estado', 'activo'),  # Valor predeterminado si no existe
                    eliminado=row.get('eliminado', 'no')  # Valor predeterminado si no existe
                )
                jugadores.append(jugador)
    except FileNotFoundError:
        raise FileNotFoundError("Archivo de jugadores no encontrado")
    except Exception as e:
        raise Exception(f"Error al leer jugadores: {e}")

    return jugadores

#Modificar estado de jugador
def modificar_estado_jugador(id_jugador: int, estado: str) -> Optional[JugadorConId]:
    jugadores = leer_todos_los_jugadores()
    for jugador in jugadores:
        if jugador.id == id_jugador:
            jugador.estado = estado
            # Guardar cambios en el archivo CSV
            with open('players.csv', mode='w', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(['id', 'nombre', 'numero', 'posicion', 'equipo', 'altura', 'edad', 'estado', 'eliminado'])  # Encabezados actualizados
                for j in jugadores:
                    escritor.writerow([j.id, j.nombre, j.numero, j.posicion, j.equipo, j.altura, j.edad, j.estado, j.eliminado])
            return jugador
    return None

#agg jugador
def agregar_jugador(jugador: JugadorConId) -> JugadorConId:
    jugadores = leer_todos_los_jugadores()
    jugador.id = max([j.id for j in jugadores], default=0) + 1  # Asignar nuevo ID
    # Asegurarse de que tenga valores predeterminados
    if not hasattr(jugador, 'estado') or jugador.estado is None:
        jugador.estado = 'activo'
    if not hasattr(jugador, 'eliminado') or jugador.eliminado is None:
        jugador.eliminado = 'no'
    jugadores.append(jugador)
    # Guardar en el archivo CSV
    with open('players.csv', mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([jugador.id, jugador.nombre, jugador.numero, jugador.posicion, jugador.equipo, jugador.altura, jugador.edad, jugador.estado, jugador.eliminado])
    return jugador

# Leer un jugador por ID
def leer_un_jugador(id_jugador: int) -> Optional[JugadorConId]:
    jugadores = leer_todos_los_jugadores()
    for jugador in jugadores:
        if jugador.id == id_jugador:
            return jugador
    return None

# Buscar jugadores por número de camiseta o apellido
def buscar_jugadores(numero_camiseta: Optional[int] = None, apellido: Optional[str] = None) -> List[JugadorConId]:
    jugadores = leer_todos_los_jugadores()
    resultados = []
    for jugador in jugadores:
        if (numero_camiseta is not None and jugador.numero == numero_camiseta) or \
                (apellido is not None and apellido.lower() in jugador.nombre.lower()):
            resultados.append(jugador)
    return resultados

# Leer todos los partidos desde el archivo CSV
def leer_todos_los_partidos() -> List[PartidoConId]:
    partidos = []
    try:
        with open('games.csv', mode='r', encoding='utf-8') as archivo:
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
                    estado=row.get('estado', 'jugado'),  # Valor predeterminado si no existe
                    eliminado=row.get('eliminado', 'no')  # Valor predeterminado si no existe
                )
                partidos.append(partido)
    except FileNotFoundError:
        raise FileNotFoundError("Archivo de partidos no encontrado")
    except Exception as e:
        raise Exception(f"Error al leer partidos: {e}")

    return partidos

# Modificar estado de partido
def modificar_estado_partido(id_partido: int, estado: str) -> Optional[PartidoConId]:
    partidos = leer_todos_los_partidos()
    for partido in partidos:
        if partido.id_partido == id_partido:
            partido.estado = estado
            # Guardar cambios en el archivo CSV
            with open('games.csv', mode='w', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(['id_partido', 'fecha', 'fase', 'rival', 'puntaje_usa', 'puntaje_rival', 'jugador_destacado', 'puntos', 'rebotes', 'asistencias', 'robos', 'minutos_jugados', 'estado', 'eliminado'])  # Encabezados
                for p in partidos:
                    escritor.writerow([p.id_partido, p.fecha, p.fase, p.rival, p.puntaje_usa, p.puntaje_rival, p.jugador_destacado, p.puntos, p.rebotes, p.asistencias, p.robos, p.minutos_jugados, p.estado, p.eliminado])
            return partido
    return None

# Agg partido
def agregar_partido(partido: PartidoConId) -> PartidoConId:
    partidos = leer_todos_los_partidos()
    partido.id_partido = max([p.id_partido for p in partidos], default=0) + 1  # Asignar nuevo ID
    # Asegurarse de que tenga valores predeterminados
    if not hasattr(partido, 'estado') or partido.estado is None:
        partido.estado = 'jugado'
    if not hasattr(partido, 'eliminado') or partido.eliminado is None:
        partido.eliminado = 'no'
    partidos.append(partido)
    # Guardar en el archivo CSV
    with open('games.csv', mode='a', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([partido.id_partido, partido.fecha, partido.fase, partido.rival, partido.puntaje_usa, partido.puntaje_rival, partido.jugador_destacado, partido.puntos, partido.rebotes, partido.asistencias, partido.robos, partido.minutos_jugados, partido.estado, partido.eliminado])
    return partido

# Obtener jugadores eliminados
def obtener_jugadores_eliminados() -> List[JugadorConId]:
    jugadores = leer_todos_los_jugadores()
    return [jugador for jugador in jugadores if jugador.eliminado == "si"]

# Obtener partidos eliminados
def obtener_partidos_eliminados() -> List[PartidoConId]:
    partidos = leer_todos_los_partidos()
    return [partido for partido in partidos if partido.eliminado == "si"]

# Leer un partido por ID
def leer_un_partido(id_partido: int) -> Optional[PartidoConId]:
    partidos = leer_todos_los_partidos()
    for partido in partidos:
        if partido.id_partido == id_partido:
            return partido
    return None

# Buscar partidos por oponente
def buscar_partidos_por_oponente(oponente: str) -> List[PartidoConId]:
    partidos = leer_todos_los_partidos()
    resultados = []
    for partido in partidos:
        if oponente.lower() in partido.rival.lower():
            resultados.append(partido)
    return resultados

def eliminar_jugador(id_jugador: int) -> Optional[JugadorConId]:
    jugadores = leer_todos_los_jugadores()
    jugador_a_eliminar = None

    for jugador in jugadores:
        if jugador.id == id_jugador:
            jugador_a_eliminar = jugador
            jugador.eliminado = "si"  # Marcar como eliminado en lugar de quitarlo de la lista
            break

    if jugador_a_eliminar:
        # Guardar la eliminación en jugelim.csv
        with open('jugelim.csv', mode='a', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([jugador_a_eliminar.id, jugador_a_eliminar.nombre, jugador_a_eliminar.numero,
                               jugador_a_eliminar.posicion, jugador_a_eliminar.equipo, jugador_a_eliminar.altura,
                               jugador_a_eliminar.edad, jugador_a_eliminar.estado, jugador_a_eliminar.eliminado])

        # Guardar los jugadores actualizados en players.csv
        with open('players.csv', mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(['id', 'nombre', 'numero', 'posicion', 'equipo', 'altura', 'edad', 'estado', 'eliminado'])  # Encabezados
            for jugador in jugadores:
                escritor.writerow(
                    [jugador.id, jugador.nombre, jugador.numero, jugador.posicion, jugador.equipo, jugador.altura,
                     jugador.edad, jugador.estado, jugador.eliminado])

        return jugador_a_eliminar
    return None

def eliminar_partido(id_partido: int) -> Optional[PartidoConId]:
    partidos = leer_todos_los_partidos()
    partido_a_eliminar = None

    for partido in partidos:
        if partido.id_partido == id_partido:
            partido_a_eliminar = partido
            partido.eliminado = "si"  # Marcar como eliminado en lugar de quitarlo de la lista
            break

    if partido_a_eliminar:
        # Guardar la eliminación en partelim.csv
        with open('partelim.csv', mode='a', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([partido_a_eliminar.id_partido, partido_a_eliminar.fecha, partido_a_eliminar.fase,
                               partido_a_eliminar.rival, partido_a_eliminar.puntaje_usa,
                               partido_a_eliminar.puntaje_rival, partido_a_eliminar.jugador_destacado,
                               partido_a_eliminar.puntos, partido_a_eliminar.rebotes, partido_a_eliminar.asistencias,
                               partido_a_eliminar.robos, partido_a_eliminar.minutos_jugados, partido_a_eliminar.estado, partido_a_eliminar.eliminado])

        # Guardar los partidos actualizados en games.csv
        with open('games.csv', mode='w', newline='', encoding='utf-8') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(
                ['id_partido', 'fecha', 'fase', 'rival', 'puntaje_usa', 'puntaje_rival', 'jugador_destacado', 'puntos',
                 'rebotes', 'asistencias', 'robos', 'minutos_jugados', 'estado', 'eliminado'])  # Encabezados
            for partido in partidos:
                escritor.writerow([partido.id_partido, partido.fecha, partido.fase, partido.rival, partido.puntaje_usa,
                                   partido.puntaje_rival, partido.jugador_destacado, partido.puntos, partido.rebotes,
                                   partido.asistencias, partido.robos, partido.minutos_jugados, partido.estado, partido.eliminado])

        return partido_a_eliminar
    return None

# Modificar información de un jugador
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
            # Guardar cambios en el archivo CSV
            with open('players.csv', mode='w', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(['id', 'nombre', 'numero', 'posicion', 'equipo', 'altura', 'edad', 'estado', 'eliminado'])  # Encabezados
                for jugador in jugadores:
                    escritor.writerow([jugador.id, jugador.nombre, jugador.numero, jugador.posicion, jugador.equipo, jugador.altura, jugador.edad, jugador.estado, jugador.eliminado])
            return j
    return None

# Modificar información de un partido
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
            # Guardar cambios en el archivo CSV
            with open('games.csv', mode='w', newline='', encoding='utf-8') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow(['id_partido', 'fecha', 'fase', 'rival', 'puntaje_usa', 'puntaje_rival', 'jugador_destacado', 'puntos', 'rebotes', 'asistencias', 'robos', 'minutos_jugados', 'estado', 'eliminado'])  # Encabezados
                for partido in partidos:
                    escritor.writerow([partido.id_partido, partido.fecha, partido.fase, partido.rival, partido.puntaje_usa, partido.puntaje_rival, partido.jugador_destacado, partido.puntos, partido.rebotes, partido.asistencias, partido.robos, partido.minutos_jugados, partido.estado, partido.eliminado])
            return p
    return None