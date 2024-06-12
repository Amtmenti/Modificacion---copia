#forms.py core\pos\model

from django import forms

from .models import *

#FORMULARIO DE LA CLASE ALUMNO

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
                'autocomplete': 'off'  # Asegura que no se autocomplete
            }),
            'periodo_termino': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'periodo_termino',
                'data-toggle': 'datetimepicker',
                'data-target': '#periodo_termino',
                'autocomplete': 'off'  # Asegura que no se autocomplete
            }),
            'token': forms.TextInput(attrs={'placeholder': 'En caso de requerir un Token especifico Ingreselo'}),
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

# FORMULARIO DE REGISTRO DE ASISTENCIA
class RegistroAsistenciaForm(forms.ModelForm):
    token = forms.CharField(max_length=8, widget=forms.TextInput(attrs={'placeholder': 'Ingresa el Token Asignado'}))

    class Meta:
        model = RegistroAsistencia
        fields = ['alumno','fecha', 'hora_entrada', 'hora_salida']
        widgets = {
            'alumno': forms.Select(attrs={'class': 'form-control select2'}),

            'fecha': forms.DateInput(format='%Y-%m-%d', attrs={
                'class': 'form-control datetimepicker-input',
                'id': 'fecha',
                'data-toggle': 'datetimepicker',
                'data-target': '#fecha',
                'autocomplete': 'off',
                'readonly': True
            }),
            'hora_entrada': forms.TimeInput(format='%H:%M', attrs={
                'class': 'form-control timepicker-input',
                'id': 'hora_entrada',
                'data-toggle': 'timepicker',
                'data-target': '#hora_entrada',
                'readonly': True
            }),
            'hora_salida': forms.TimeInput(format='%H:%M', attrs={
                'class': 'form-control timepicker-input',
                'id': 'hora_salida',
                'data-toggle': 'timepicker',
                'data-target': '#hora_salida',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['token'].widget.attrs['autofocus'] = True

    def clean_token(self):
        token = self.cleaned_data.get('token')
        if not Alumno.objects.filter(token=token).exists():
            raise forms.ValidationError("Token no válido")
        return token

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                token = self.cleaned_data.get('token')
                alumno = Alumno.objects.get(token=token)
                instance = super().save(commit=False)
                instance.alumno = alumno
                if commit:
                    instance.save()
                data = instance.toJSON()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data
