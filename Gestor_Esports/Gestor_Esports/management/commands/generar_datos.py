# generar_datos.py
# Ejecutar con:
#   python manage.py runscript generar_datos
# o (si no usas django-extensions):
#   python manage.py shell < generar_datos.py

import random
from decimal import Decimal
from datetime import date, timedelta
from faker import Faker

from django.db import transaction

# Ajusta aquí cuántos elementos quieres generar
NUM = 10

fake = Faker()
Faker.seed(0)
random.seed(0)

def random_date_between(start_days_ago=1000, end_days_from_start=365):
    start = date.today() - timedelta(days=random.randint(0, start_days_ago))
    end = start + timedelta(days=random.randint(1, end_days_from_start))
    return start, end

def run():
    from Gestor_Esports.models import (
        Usuario, Perfil, Equipo, Jugador, Juego, Torneo,
        Patrocinador, Contrato, EstadisticaJugador, Participacion
    )

    usuarios_count = max( NUM * 2, 20 )     # suficientes usuarios para perfiles + jugadores
    juegos_count = NUM
    patrocinadores_count = NUM
    equipos_count = NUM
    jugadores_count = NUM
    torneos_count = NUM

    print("Borrando datos antiguos (opcional). Si no quieres esto, comenta la sección.")
    # Si no quieres borrar datos, comenta las siguientes líneas
    Usuario.objects.all().delete()
    Perfil.objects.all().delete()
    Jugador.objects.all().delete()
    Juego.objects.all().delete()
    Torneo.objects.all().delete()
    Equipo.objects.all().delete()
    Patrocinador.objects.all().delete()
    Contrato.objects.all().delete()
    EstadisticaJugador.objects.all().delete()
    Participacion.objects.all().delete()

    with transaction.atomic():
        # Usuarios + Perfiles
        usuarios = []
        for i in range(usuarios_count):
            nombre = fake.name()
            email = fake.unique.email()
            u = Usuario.objects.create(
                nombre=nombre,
                email=email,
                activo= random.choice([True]*9 + [False])  # la mayoría activos
            )
            # Perfil (fecha_nacimiento puede ser None por modelo)
            Perfil.objects.create(
                usuario=u,
                biografia=fake.sentence(nb_words=12),
                pais=fake.country(),
                fecha_nacimiento = fake.date_between(start_date='-40y', end_date='-16y') if random.random() > 0.1 else None,
                avatar=None
            )
            usuarios.append(u)
        print(f"Usuarios creados: {len(usuarios)}")

        # Juegos
        juegos = []
        for _ in range(juegos_count):
            j = Juego.objects.create(
                nombre = fake.unique.word().capitalize() + " " + fake.word().capitalize(),
                genero = random.choice(['MOBA','FPS','FPS','RTS','Battle Royale','Deportes','RPG']),
                desarrolladora = fake.company(),
                fecha_lanzamiento = fake.date_between(start_date='-10y', end_date='today')
            )
            juegos.append(j)
        print(f"Juegos creados: {len(juegos)}")

        # Patrocinadores
        patrocinadores = []
        for _ in range(patrocinadores_count):
            p = Patrocinador.objects.create(
                nombre = fake.company(),
                industria = fake.bs(),
                pais = fake.country(),
                presupuesto_anual = float(round(random.uniform(50000, 2_000_000), 2))
            )
            patrocinadores.append(p)
        print(f"Patrocinadores creados: {len(patrocinadores)}")

        # Equipos
        equipos = []
        for _ in range(equipos_count):
            eq = Equipo.objects.create(
                nombre = fake.unique.company(),
                fecha_creacion = fake.date_between(start_date='-10y', end_date='today'),
                pais = fake.country(),
                presupuesto = Decimal(str(round(random.uniform(5000, 200000), 2)))
            )
            equipos.append(eq)
        print(f"Equipos creados: {len(equipos)}")

        # Contratos (through) -> asignar 1-3 patrocinadores por equipo, evitando duplicados
        contratos = []
        for equipo in equipos:
            n = random.randint(1, min(3, len(patrocinadores)))
            chosen = random.sample(patrocinadores, n)
            for pat in chosen:
                fecha_inicio, fecha_fin = random_date_between(start_days_ago=1000, end_days_from_start=365)
                monto = Decimal(str(round(random.uniform(500, 50000), 2)))
                c = Contrato.objects.create(
                    equipo=equipo,
                    patrocinador=pat,
                    fecha_inicio=fecha_inicio,
                    fecha_fin=fecha_fin,
                    monto=monto
                )
                contratos.append(c)
        print(f"Contratos creados: {len(contratos)}")

        # Jugadores: usar usuarios distintos (OneToOne). Tomamos una muestra de usuarios.
        jugadores = []
        posible_usuarios = usuarios[:]  # lista clon
        random.shuffle(posible_usuarios)
        for i in range(jugadores_count):
            if not posible_usuarios:
                break
            u = posible_usuarios.pop()
            nickname = fake.user_name()[:30]
            equipo = random.choice(equipos + [None]) if random.random() < 0.85 else None  # la mayoría en equipo, algunos sin equipo
            j = Jugador.objects.create(
                usuario=u,
                equipo = equipo,
                nickname = nickname,
                rol = random.choice(['Top','Mid','ADC','Support','Jungla','Shotcaller','Coach']),
                nacionalidad = fake.country()
            )
            jugadores.append(j)
        print(f"Jugadores creados: {len(jugadores)}")

        # EstadisticaJugador: uno a uno con jugador
        for j in jugadores:
            partidas = random.randint(0, 200)
            victorias = random.randint(0, partidas)
            derrotas = partidas - victorias
            kda = round(random.uniform(0.5, 10.0), 2) if partidas>0 else 0.0
            EstadisticaJugador.objects.create(
                jugador = j,
                partidas_jugadas = partidas,
                victorias = victorias,
                derrotas = derrotas,
                kda_promedio = kda
            )
        print(f"Estadísticas creadas para jugadores: {len(jugadores)}")

        # Torneos
        torneos = []
        for _ in range(torneos_count):
            juego = random.choice(juegos)
            fecha_inicio, fecha_fin = random_date_between(start_days_ago=500, end_days_from_start=60)
            t = Torneo.objects.create(
                nombre = f"{fake.city()} {random.randint(1,999)} Cup",
                juego = juego,
                fecha_inicio = fecha_inicio,
                fecha_fin = fecha_fin,
                premio_total = Decimal(str(round(random.uniform(1000, 200000), 2)))
            )
            torneos.append(t)
        print(f"Torneos creados: {len(torneos)}")

        # Participaciones: para cada torneo, 2- min(6, equipos_count) equipos distintos
        participaciones_creadas = 0
        for torneo in torneos:
            num_participantes = random.randint(2, min(6, len(equipos)))
            participantes = random.sample(equipos, num_participantes)
            # generar puntos aleatorios y ordenar para dar posicion
            puntos_map = {e: random.randint(0, 100) for e in participantes}
            # ordenar por puntos desc para asignar posicion_final
            orden = sorted(participantes, key=lambda e: puntos_map[e], reverse=True)
            for pos_idx, equipo in enumerate(orden, start=1):
                puntos = puntos_map[equipo]
                # Evitar duplicados (unique_together)
                if Participacion.objects.filter(equipo=equipo, torneo=torneo).exists():
                    continue
                Participacion.objects.create(
                    equipo = equipo,
                    torneo = torneo,
                    posicion_final = pos_idx,
                    puntos_obtenidos = puntos
                )
                participaciones_creadas += 1
        print(f"Participaciones creadas: {participaciones_creadas}")

    print("Seeding completado correctamente.")
    print(f"Resumen: Usuarios={len(usuarios)}, Juegos={len(juegos)}, Patrocinadores={len(patrocinadores)}, "
          f"Equipos={len(equipos)}, Contratos={len(contratos)}, Jugadores={len(jugadores)}, Torneos={len(torneos)}, "
          f"Participaciones={participaciones_creadas}")
