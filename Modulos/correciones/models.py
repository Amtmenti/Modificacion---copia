#model del core\pos

import os
import secrets

from datetime import datetime, timedelta
from config import settings
from django.forms import model_to_dict
from core.pos.choices import Modalidad
from django.db import models

# Función para generar un token único
def generate_unique_token():
    return secrets.token_urlsafe(6)[:8]

# Modelo Alumno
class Alumno(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre')
    telefono = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfono')
    email = models.CharField(max_length=50, null=True, blank=True, verbose_name='Email')
    modalidad = models.CharField(max_length=50, choices=Modalidad, default=Modalidad[0][0][0], verbose_name='Modalidad')
    periodo_inicio = models.DateField(default=datetime.now, verbose_name='Fecha de Inicio')
    periodo_termino = models.DateField(default=datetime.now, verbose_name='Fecha de Termino')
    token = models.CharField(default=generate_unique_token, max_length=8, unique=True, editable=True, verbose_name='Token para el Alumno')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.nombre} ({self.modalidad})'

    def periodo_inicio_format(self):
        return self.periodo_inicio.strftime('%Y-%m-%d')

    def periodo_termino_format(self):
        return self.periodo_termino.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['text'] = self.get_full_name()
        item['modalidad'] = {'id': self.modalidad, 'name': self.get_modalidad_display()}
        item['periodo_inicio'] = self.periodo_inicio.strftime('%Y-%m-%d')
        item['periodo_termino'] = self.periodo_termino.strftime('%Y-%m-%d')
        item['token'] = self.token
        return item

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        super().save(*args, **kwargs)

    def generate_token(self):
        return generate_unique_token()

    class Meta:
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'

# Modelo RegistroAsistencia
class RegistroAsistencia(models.Model):
    alumno = models.ForeignKey('Alumno', on_delete=models.CASCADE, verbose_name='Alumno')
    fecha = models.DateField(default=datetime.now, verbose_name='Fecha')
    hora_entrada = models.TimeField(default=datetime.now, verbose_name='Hora de Entrada')
    hora_salida = models.TimeField(null=True, blank=True, verbose_name='Hora de Salida')

    def __str__(self):
        return self.get_full_entrada() if not self.hora_salida else self.get_full_salida()

    def get_full_entrada(self):
        return f'Asistencia de {self.alumno.get_full_name()} el {self.fecha.strftime("%Y-%m-%d")} a las {self.hora_entrada.strftime("%H:%M")}'

    def get_full_salida(self):
        return f'Salida de {self.alumno.get_full_name()} el {self.fecha.strftime("%Y-%m-%d")} a las {self.hora_salida.strftime("%H:%M")}'

    def fecha_format(self):
        return self.fecha.strftime('%Y-%m-%d')

    def save(self, *args, **kwargs):
        if not self.pk:  # Si es un nuevo registro
            self.hora_entrada = datetime.now().time()
        else:  # Validación para evitar registros incorrectos de salida
            if self.hora_salida and not self.hora_entrada:
                raise ValueError("No se puede registrar una salida sin una entrada correspondiente.")
        super().save(*args, **kwargs)

    def calcular_total_horas(self):
        if self.hora_salida:
            if self.hora_salida and self.hora_salida <= self.hora_entrada:
                raise ValueError("La hora de salida debe ser posterior a la hora de entrada.")
            hora_entrada_dt = datetime.combine(self.fecha, self.hora_entrada)
            if self.hora_salida and not self.hora_entrada:
                raise ValueError("No se puede registrar una salida sin una entrada correspondiente.")
            hora_salida_dt = datetime.combine(self.fecha, self.hora_salida)
            total_horas = hora_salida_dt - hora_entrada_dt
            total_segundos = total_horas.total_seconds()
            horas = int(total_segundos // 3600)
            minutos = int((total_segundos % 3600) // 60)
            return f'{horas} horas, {minutos} minutos'
        return 'Hora de salida no registrada'

    def toJSON(self):
        item = model_to_dict(self)
        item['text'] = self.__str__()
        item['alumno'] = self.alumno.toJSON()
        item['fecha'] = self.fecha.strftime('%Y-%m-%d')
        item['hora_entrada'] = self.hora_entrada.strftime('%H:%M')
        item['hora_salida'] = self.hora_salida.strftime('%H:%M') if self.hora_salida else None
        item['total_horas'] = self.calcular_total_horas()
        return item

    class Meta:
        verbose_name = 'Registro de Asistencia'
        verbose_name_plural = 'Registros de Asistencia'
