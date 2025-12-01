from faker import Faker
import random
from datetime import timedelta
from django.core.management.base import BaseCommand

from Gestor_Esports.models import (
    Juego, Plataforma, Equipo, Jugador, PerfilJugador,
    Torneo, Partido, ResultadoPartido, Sponsor, InscripcionTorneo
)

class Command(BaseCommand):
    help = "Genera datos de prueba con Faker"

    def handle(self, *args, **kwargs):
        self.generar_datos()
        self.stdout.write(self.style.SUCCESS("Datos Faker generados correctamente."))

    def generar_datos(self):
        fake = Faker()

#Registros a crear

fake = Faker()

juegos = []
for _ in range(10):
    juego = Juego.objects.create(
        nombre=fake.unique.word().capitalize() + " Arena",
        descripcion=fake.text(),
        genero=random.choice(["FPS", "MOBA", "Battle Royale", "Deporte", "Lucha"]),
        fecha_lanzamiento=fake.date_between(start_date="-10y", end_date="today"),
    )
    juegos.append(juego)

plataformas = []
for _ in range(10):
    plataforma = Plataforma.objects.create(
        nombre=fake.unique.company(),
        fabricante=fake.company(),
        sitio_web=fake.url(),
        activa=random.choice([True, True, False]),
    )
    plataformas.append(plataforma)

equipos = []
for _ in range(10):
    equipo = Equipo.objects.create(
        nombre=fake.unique.company() + " Esports",
        pais=fake.country(),
        fecha_creacion=fake.date_between(start_date="-5y", end_date="today"),
    )
    equipo.juegos.set(random.sample(juegos, k=random.randint(1, 3)))
    equipos.append(equipo)

jugadores = []
for _ in range(10):
    jugador = Jugador.objects.create(
        nickname=fake.unique.user_name(),
        nombre_real=fake.name(),
        edad=random.randint(14, 35),
        equipo=random.choice(equipos),
        rol=random.choice(["tank", "dps", "support", "igl"]),
    )
    jugadores.append(jugador)

for jugador in jugadores:
    PerfilJugador.objects.create(
        jugador=jugador,
        biografia=fake.text(),
        twitter=fake.url(),
        sensibilidad_raton=round(random.uniform(0.5, 2.5), 2),
        dpi=random.choice([400, 800, 1600, 3200]),
    )

torneos = []
for _ in range(10):
    torneo = Torneo.objects.create(
        nombre=fake.unique.catch_phrase() + " Cup",
        juego=random.choice(juegos),
        fecha_inicio=fake.date_between(start_date="-1y", end_date="today"),
        fecha_fin=fake.date_between(start_date="today", end_date="+30d"),
        premio_total=random.randint(1000, 50000),
    )
    torneo.plataformas.set(random.sample(plataformas, k=random.randint(1, 3)))
    torneos.append(torneo)

partidos = []
for _ in range(10):
    eq1, eq2 = random.sample(equipos, 2)
    partido = Partido.objects.create(
        torneo=random.choice(torneos),
        equipo_local=eq1,
        equipo_visitante=eq2,
        fecha=fake.date_time_this_year(),
        finalizado=random.choice([True, False]),
    )
    partidos.append(partido)

for partido in partidos:
    if partido.finalizado:
        ResultadoPartido.objects.create(
            partido=partido,
            puntuacion_local=random.randint(0, 3),
            puntuacion_visitante=random.randint(0, 3),
            duracion=timedelta(minutes=random.randint(20, 60)),
            mvp=random.choice(jugadores),
        )

sponsors = []
for _ in range(10):
    sponsor = Sponsor.objects.create(
        nombre=fake.unique.company() + " Corp",
        sector=random.choice(["Tecnología", "Bebidas", "Gaming", "Hardware"]),
        sitio_web=fake.url(),
    )
    sponsor.equipos.set(random.sample(equipos, k=random.randint(1, 3)))
    sponsors.append(sponsor)

for _ in range(10):
    InscripcionTorneo.objects.get_or_create(
        equipo=random.choice(equipos),
        torneo=random.choice(torneos),
        defaults={
            "cuota_pagada": random.choice([True, False]),
            "posicion_final": random.randint(1, 16),
        }
    )