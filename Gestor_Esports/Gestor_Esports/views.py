# Gestor_Esports/views.py
from django.shortcuts import render

def index(request):
    # Renderiza el template que se ve en tu captura:
    return render(request, 'Gestor_Esports/dj_index.html')