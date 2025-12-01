from django.contrib import admin
from .models import InscripcionTorneo, Juego, Plataforma, Equipo, Jugador, PerfilJugador, Sponsor, Torneo, Partido, ResultadoPartido

# Register your models here.

admin.site.register(Juego)
admin.site.register(Plataforma)
admin.site.register(Equipo)
admin.site.register(Jugador)
admin.site.register(PerfilJugador)
admin.site.register(Torneo)
admin.site.register(Partido)
admin.site.register(ResultadoPartido)
admin.site.register(Sponsor)
admin.site.register(InscripcionTorneo)