from django.urls import path

from core.pos.views.alumno.views import *
from core.pos.views.asistencia.views import *

urlpatterns = [
    # Alumno
    path('alumno/', AlumnoListView.as_view(), name='alumno_list'),
    path('alumno/add/', AlumnoCreateView.as_view(), name='alumno_create'),
    path('alumno/update/<int:pk>/', AlumnoUpdateView.as_view(), name='alumno_update'),
    path('alumno/delete/<int:pk>/', AlumnoDeleteView.as_view(), name='alumno_delete'),

    # URLs para Registro de Entrada
    path('entrada/', RegistroEntradaListView.as_view(), name='entrada_list'),
    path('entrada/add/', RegistroEntradaCreateView.as_view(), name='entrada_create'),

    # URLs para Registro de Salida
    path('salida/', RegistroSalidaListView.as_view(), name='salida_list'),
    path('salida/add/', RegistroSalidaCreateView.as_view(), name='salida_create'),
]