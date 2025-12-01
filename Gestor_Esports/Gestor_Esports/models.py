from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class Juego(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    genero = models.CharField(max_length=80)
    fecha_lanzamiento = models.DateField(null=True, blank=True)
    
class Plataforma(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    fabricante = models.CharField(max_length=100)
    sitio_web = models.URLField(null=True, blank=True)
    activa = models.BooleanField(default=True)

class Equipo(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    pais = models.CharField(max_length=80)
    fecha_creacion = models.DateField()
    juegos = models.ManyToManyField(Juego, related_name='equipos', blank=True)

class Jugador(models.Model):
    nickname = models.CharField(max_length=80, unique=True)
    nombre_real = models.CharField(max_length=120)
    edad = models.IntegerField(validators=[MinValueValidator(12)])
    equipo = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, related_name='jugadores')
    rol = models.CharField(max_length=60,
                           choices=[('tank', 'Tanque'),
                                    ('dps', 'DPS'),
                                    ('support', 'Soporte'),
                                    ('igl', 'In-Game Leader')])

class PerfilJugador(models.Model):
    jugador = models.OneToOneField(Jugador, on_delete=models.CASCADE, related_name='perfil')
    biografia = models.TextField(blank=True)
    twitter = models.URLField(null=True, blank=True)
    sensibilidad_raton = models.DecimalField(max_digits=4, decimal_places=2, default=1.00)
    dpi = models.IntegerField(default=800)

class Torneo(models.Model):
    nombre = models.CharField(max_length=150, unique=True)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='torneos')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    premio_total = models.DecimalField(max_digits=10, decimal_places=2)
    plataformas = models.ManyToManyField(Plataforma, related_name='torneos', blank=True)

class Partido(models.Model):
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='partidos')
    equipo_local = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_local')
    equipo_visitante = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_visitante')
    fecha = models.DateTimeField()
    finalizado = models.BooleanField(default=False)

class ResultadoPartido(models.Model):
    partido = models.OneToOneField(Partido, on_delete=models.CASCADE, related_name='resultado')
    puntuacion_local = models.IntegerField()
    puntuacion_visitante = models.IntegerField()
    duracion = models.DurationField(null=True, blank=True)
    mvp = models.ForeignKey(Jugador, null=True, blank=True, on_delete=models.SET_NULL, related_name='mvps')

class Sponsor(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    sector = models.CharField(max_length=100)
    sitio_web = models.URLField(blank=True, null=True)
    equipos = models.ManyToManyField(Equipo, related_name='sponsors', blank=True)

class InscripcionTorneo(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='inscripciones')
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE, related_name='inscripciones')
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)
    cuota_pagada = models.BooleanField(default=False)
    posicion_final = models.IntegerField(null=True, blank=True)

    
class Meta:
        unique_together = ('equipo', 'torneo')
