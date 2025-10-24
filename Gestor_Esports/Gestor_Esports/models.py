from django.db import models

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
    pais = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return f"Perfil de {self.usuario.nombre}"


class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateField()
    pais = models.CharField(max_length=50)
    presupuesto = models.DecimalField(max_digits=10, decimal_places=2)
    patrocinadores = models.ManyToManyField('Patrocinador', through='Contrato', related_name='equipos')

    def __str__(self):
        return self.nombre


class Jugador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="jugador")
    equipo = models.ForeignKey(Equipo, on_delete=models.SET_NULL, null=True, related_name="jugadores")
    nickname = models.CharField(max_length=50)
    rol = models.CharField(max_length=50)
    nacionalidad = models.CharField(max_length=50)
    juegos = models.ManyToManyField('Juego', related_name='jugadores')

    def __str__(self):
        return self.nickname


class Juego(models.Model):
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    desarrolladora = models.CharField(max_length=100)
    fecha_lanzamiento = models.DateField()

    def __str__(self):
        return self.nombre


class Torneo(models.Model):
    nombre = models.CharField(max_length=100)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name="torneos")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    premio_total = models.DecimalField(max_digits=8, decimal_places=2)
    equipos = models.ManyToManyField('Equipo', through='Participacion', related_name='torneos')

    def __str__(self):
        return self.nombre


class Participacion(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE)
    posicion_final = models.PositiveIntegerField()
    puntos_obtenidos = models.IntegerField()

    class Meta:
        unique_together = ('equipo', 'torneo')

    def __str__(self):
        return f"{self.equipo.nombre} en {self.torneo.nombre}"


class Patrocinador(models.Model):
    nombre = models.CharField(max_length=100)
    industria = models.CharField(max_length=100)
    pais = models.CharField(max_length=50)
    presupuesto_anual = models.FloatField()

    def __str__(self):
        return self.nombre


class Contrato(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    patrocinador = models.ForeignKey(Patrocinador, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    monto = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return f"Contrato {self.patrocinador.nombre} - {self.equipo.nombre}"


class EstadisticaJugador(models.Model):
    jugador = models.OneToOneField(Jugador, on_delete=models.CASCADE, related_name="estadisticas")
    partidas_jugadas = models.IntegerField()
    victorias = models.IntegerField()
    derrotas = models.IntegerField()
    kda_promedio = models.FloatField()

    def __str__(self):
        return f"Stats de {self.jugador.nickname}"
