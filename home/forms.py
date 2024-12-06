from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm

class EstablecimientoForm(forms.ModelForm):
    class Meta:
        model = Establecimiento
        fields = '__all__'
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del establecimiento'}),
            'Direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la dirección'}),
            'Telefono': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el teléfono'}),
            'Correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
        }

class AdministradorForm(forms.ModelForm):
    class Meta:
        model = Administrador
        fields = '__all__'
        widgets = {
            'Nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre del administrador'}),
            'Usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el nombre de usuario'}),
            'Contraseña': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la contraseña'}),
            'ID_Establecimiento': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Seleccione el establecimiento'})
        }

class EncuestaForm(forms.ModelForm):
    class Meta:
        model = Encuesta
        fields = ['Titulo', 'Descripcion']
        widgets = {
            'Titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el título de la encuesta'}),
            'Descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ingrese la descripción de la encuesta'})
        }

class PreguntaForm(forms.ModelForm):
    class Meta:
        model = Pregunta
        fields = ['Titulo']
        widgets = {
            'Titulo': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Ingrese la pregunta'
            })
        }

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = '__all__'
        widgets = {
            'Respuesta': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 9, 'placeholder': 'Ingrese un número del 1 al 9'}),
            'ID_Pregunta': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Seleccione la pregunta'})
        }

class EncuestadoForm(forms.ModelForm):
    class Meta:
        model = Encuestado
        fields = '__all__'
        widgets = {
            'Correo': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'ejemplo@correo.com'})
        }
class AdministradorRegistroForm(UserCreationForm):
    nombre = forms.CharField(
        max_length=35,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su nombre'
        })
    )
    establecimiento = forms.ModelChoiceField(
        queryset=Establecimiento.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Seleccione el establecimiento'
        }),
        required=True
    )

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('nombre', 'establecimiento')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese nombre de usuario',
                'required': True,
                'maxlength': '150',
                'help_text': 'Requerido. 150 caracteres como máximo. Únicamente letras, dígitos y @/./+/-/_.'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese contraseña',
                'required': True,
                'help_text': 'Su contraseña no puede asemejarse tanto a su otra información personal. Su contraseña debe contener al menos 8 caracteres. Su contraseña no puede ser una clave utilizada comúnmente. Su contraseña no puede ser completamente numérica.'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Confirme contraseña',
                'required': True,
                'help_text': 'Para verificar, introduzca la misma contraseña anterior.'
            })
        }
