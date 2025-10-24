from django.contrib import admin
from .models import Usuario, Perfil, Equipo, Jugador, Juego, Torneo, Patrocinador, Contrato

# Register your models here.


admin.site.register(Usuario)
admin.site.register(Perfil)
admin.site.register(Equipo)
admin.site.register(Jugador)
admin.site.register(Juego)
admin.site.register(Torneo)
admin.site.register(Patrocinador)
admin.site.register(Contrato)