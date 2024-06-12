import os
import secrets

from datetime import datetime, timedelta
from django.db import models
from config import settings
from django.forms import model_to_dict
from core.pos.choices import Modalidad

def generate_unique_token():
    return secrets.token_urlsafe(6)[:8]
    
class Alumno(models.Model):
    nombre = models.CharField(max_length=150, verbose_name='Nombre')
    telefono = models.CharField(max_length=10, null=True, blank=True, verbose_name='Teléfono')
    email = models.CharField(max_length=50, null=True, blank=True, verbose_name='Email')
    modalidad = models.CharField(max_length=50, choices=Modalidad, default=Modalidad[0][0][0], verbose_name='Modalidad')
    periodo_inicio = models.DateField(default=datetime.now, verbose_name='Fecha de Inicio')
    periodo_termino = models.DateField(default=datetime.now, verbose_name='Fecha de Termino')
    token = models.CharField(default=generate_unique_token, max_length=8, unique=True, editable=True, verbose_name='Token para el Alumno')
    horas_totales = models.DurationField(null=True, blank=True, verbose_name='Horas Totales de Estadia')

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
        itemm['token'] = self.token
        item['horas_totales'] = str(self.horas_totales) if self.horas_totales else '00:00:00'
        return item

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self.generate_token()
        super().save(*args, **kwargs)

    def generate_token(self):
        return generate_unique_token()


class RegistroEntrada(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='entradas_alumno')
    fecha_e = models.DateField(default=datetime.now, verbose_name='Fecha')
    hora_entrada = models.TimeField(default=datetime.now, verbose_name='Hora de Entrada')
    token = models.CharField(max_length=8, verbose_name='Token de Validación')

    def hora_entrada_format(self):
        return self.hora_cita.strftime('%H:%M')

    def fecha_e_format(self):
        return self.periodo_termino.strftime('%Y-%m-%d')
    
    def save(self, *args, **kwargs):
        # Validacion
        if self.alumno.token != self.token:
            raise ValueError("Token inválido para el alumno seleccionado.")

        # Registro doble
        if RegistroSalida.objects.filter(alumno=self.alumno, fecha=self.fecha).exists():
            raise ValueError("Ya existe una salida registrada para este alumno en esta fecha.")

        super().save(*args, **kwargs)


class RegistroSalida(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='salidas_alumno')
    fecha_s = models.DateField(default=datetime.now, verbose_name='Fecha')
    hora_salida = models.TimeField(default=datetime.now, verbose_name='Hora de Salida')
    token = models.CharField(max_length=8, verbose_name='Token de Validación')

    def fecha_s_format(self):
        return self.periodo_inicio.strftime('%Y-%m-%d')

    def save(self, *args, **kwargs):
        # Validacion
        if self.alumno.token != self.token:
            raise ValueError("Token inválido para el alumno seleccionado.")

        # Registro doble
        try:
            entrada = RegistroEntrada.objects.get(alumno=self.alumno, fecha=self.fecha)
        except RegistroEntrada.DoesNotExist:
            raise ValueError("No existe un registro de entrada para este alumno en esta fecha.")

        # Calculo del tiempo total
        entrada_datetime = datetime.combine(entrada.fecha, entrada.hora_entrada)
        salida_datetime = datetime.combine(self.fecha, self.hora_salida)
        delta = salida_datetime - entrada_datetime

        if self.alumno.horas_totales:
            self.alumno.horas_totales += delta
        else:
            self.alumno.horas_totales = delta

        self.alumno.save()
        super().save(*args, **kwargs)
