from django.urls import path

from core.pos.views.alumno.views import *
from core.pos.views.horario.views import *

urlpatterns = [
    # Alumno
    path('alumno/', AlumnoListView.as_view(), name='alumno_list'),
    path('alumno/add/', AlumnoCreateView.as_view(), name='alumno_create'),
    path('alumno/update/<int:pk>/', AlumnoUpdateView.as_view(), name='alumno_update'),
    path('alumno/delete/<int:pk>/', AlumnoDeleteView.as_view(), name='alumno_delete'),

    # Horario
    path('horario/', HorarioListView.as_view(), name='horario_list'),
    path('horario/add/', HorarioCreateView.as_view(), name='horario_create'),
    path('horario/update/<int:pk>/', HorarioUpdateView.as_view(), name='horario_update'),
    path('horario/delete/<int:pk>/', HorarioDeleteView.as_view(), name='horario_delete'),

]