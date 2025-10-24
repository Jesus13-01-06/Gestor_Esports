from django.db import models
from datetime import date
from decimal import Decimal

class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    fecha_registro = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Perfil(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="perfil")
    biografia = models.TextField(blank=True)
    pais = models.CharField(max_length=50, blank=True)           # permito blank para facilitar el seed
    fecha_nacimiento = models.DateField(null=True, blank=True)   # permito null para que el seeder no falle
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.nombre}"


class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateField(default=date.today)                        # default para el seeder
    pais = models.CharField(max_length=50, blank=True)
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('10000.00'))
    patrocinadores = models.ManyToManyField('Patrocinador', through='Contrato', related_name='equipos')

    def __str__(self):
        return self.nombre


class Jugador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="jugador")
    equipo = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, related_name="jugadores")
    nickname = models.CharField(max_length=50)
    rol = models.CharField(max_length=50, blank=True)
    nacionalidad = models.CharField(max_length=50, blank=True)
    juegos = models.ManyToManyField('Juego', related_name='jugadores')

    def __str__(self):
        return self.nickname


class Juego(models.Model):
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=50, blank=True)
    desarrolladora = models.CharField(max_length=100, blank=True)
    fecha_lanzamiento = models.DateField(default=date.today)    # default para el seeder

    def __str__(self):
        return self.nombre


class Torneo(models.Model):
    nombre = models.CharField(max_length=100)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name="torneos")
    fecha_inicio = models.DateField(default=date.today)
    fecha_fin = models.DateField(default=date.today)
    premio_total = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('1000.00'))
    equipos = models.ManyToManyField('Equipo', through='Participacion', related_name='torneos')

    def __str__(self):
        return self.nombre


class Participacion(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE)
    posicion_final = models.PositiveIntegerField(default=0)   # default para que no falle el NOT NULL
    puntos_obtenidos = models.IntegerField(default=0)         # default para que no falle el NOT NULL

    class Meta:
        unique_together = ('equipo', 'torneo')

    def __str__(self):
        return f"{self.equipo.nombre} en {self.torneo.nombre}"


class Patrocinador(models.Model):
    nombre = models.CharField(max_length=100)
    industria = models.CharField(max_length=100, blank=True)
    pais = models.CharField(max_length=50, blank=True)
    presupuesto_anual = models.FloatField(default=100000.0)

    def __str__(self):
        return self.nombre


class Contrato(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    patrocinador = models.ForeignKey(Patrocinador, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=date.today)
    fecha_fin = models.DateField(default=date.today)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1000.00'))

    def __str__(self):
        return f"Contrato {self.patrocinador.nombre} - {self.equipo.nombre}"


class EstadisticaJugador(models.Model):
    jugador = models.OneToOneField(Jugador, on_delete=models.CASCADE, related_name="estadisticas")
    partidas_jugadas = models.IntegerField(default=0)
    victorias = models.IntegerField(default=0)
    derrotas = models.IntegerField(default=0)
    kda_promedio = models.FloatField(default=0.0)

    def __str__(self):
        return f"Stats de {self.jugador.nickname}"
