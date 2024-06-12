from django.db import models
from datetime import datetime
from django.forms import model_to_dict
import secrets
from core.pos.choices import Modalidad, Dias

def generate_unique_token():
    return secrets.token_urlsafe(6)[:8]

class Alumno(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre')
    telefono = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfono')
    email = models.CharField(max_length=50, null=True, blank=True, verbose_name='Email')
    modalidad = models.CharField(max_length=50, choices=Modalidad, default=Modalidad[0][0], verbose_name='Modalidad')
    periodo_inicio = models.DateField(default=datetime.now, verbose_name='Fecha de Inicio')
    periodo_termino = models.DateField(default=datetime.now, verbose_name='Fecha de Termino')
    token = models.CharField(default=generate_unique_token, max_length=8, unique=True, editable=True, verbose_name='Token para el Alumno')
    horas_totales = models.DurationField(null=True, blank=True, verbose_name='Horas Totales de Estadia')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.nombre}'

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
        item['horas_totales'] = str(self.horas_totales) if self.horas_totales else '00:00:00'
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

class Horario(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='horarios')
    nombre_alumno = models.CharField(null=True, max_length=150, verbose_name='Nombre del Alumno')
    dia = models.CharField(max_length=10, choices=Dias, verbose_name='Día de la Semana')
    habilitado = models.BooleanField(default=False, verbose_name='Habilitado')
    hentrada = models.TimeField(verbose_name='Hora de entrada')
    hsalida = models.TimeField(null=True, verbose_name='Hora de salida')

    def __str__(self):
        return f'{self.get_dia_display()} - {self.nombre_alumno}'

    def hentrada_format(self):
        return self.hentrada.strftime('%H:%M')

    def hsalida_format(self):
        return self.hsalida.strftime('%H:%M')

    def toJSON(self):
        item = model_to_dict(self)
        item['dia'] = self.get_dia_display()
        item['hentrada'] = self.hentrada_format()
        item['hsalida'] = self.hsalida_format()
        item['habilitado'] = self.habilitado
        return item

    def save(self, *args, **kwargs):
        self.nombre_alumno = self.alumno.nombre  # Actualiza el nombre del alumno
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
