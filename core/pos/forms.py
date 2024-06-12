from django import forms
from .models import Alumno, Horario
from datetime import datetime

# FORMULARIO DE LA CLASE ALUMNO
class AlumnoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Alumno
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre del Alumno'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese un email'}),
            'periodo_inicio': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'periodo_inicio',
                'data-toggle': 'datetimepicker',
                'data-target': '#periodo_inicio',
                'autocomplete': 'off'
            }),
            'periodo_termino': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'periodo_termino',
                'data-toggle': 'datetimepicker',
                'data-target': '#periodo_termino',
                'autocomplete': 'off'
            }),
            'token': forms.TextInput(attrs={'placeholder': 'En caso de requerir un Token especifico Ingreselo'}),
            'duracion_periodo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Introduzca el siguiente formato: (Horas:Minutos:Segundos)',
            }),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                instance = super().save(commit=False)
                if not instance.token:
                    instance.token = instance.generate_token()
                if commit:
                    instance.save()
                data = instance.toJSON()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class HorarioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['alumno'].widget.attrs['autofocus'] = True

    class Meta:
        model = Horario
        fields = '__all__'
        widgets = {
            'alumno': forms.Select(attrs={
                'class': 'select2',
                'style': 'width: 100%'
            }),
            'dia': forms.Select(attrs={
                'class': 'select2',
                'style': 'width: 100%'
            }),
            'habilitado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hentrada': forms.TimeInput(format='%H:%M', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'hentrada',
                'value': datetime.now().strftime('%H:%M'),
                'data-toggle': 'datetimepicker',
                'data-target': '#hentrada'
            }),
            'hsalida': forms.TimeInput(format='%H:%M', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'hsalida',
                'value': datetime.now().strftime('%H:%M'),
                'data-toggle': 'datetimepicker',
                'data-target': '#hsalida'
            }), 
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                instance = super().save(commit=False)
                instance.nombre_alumno = instance.alumno.nombre  # Actualiza el nombre del alumno
                if commit:
                    instance.save()
                data = instance.toJSON()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data
