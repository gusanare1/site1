from django import forms
from django.forms import ModelForm
from .models import Carro, Color, Marca, Modelo, Ciudad, Provincia, Persona

class PersonaForm(ModelForm):
	exclude = ('id')

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class CarroForm(ModelForm):
	#fields = ('anio','precio','esta_inspeccionado', )
	provincia = forms.ModelChoiceField(queryset = Provincia.objects.all(), empty_label=None)
	color = forms.ModelChoiceField(queryset = Color.objects.all(), empty_label=None)
	ciudad = forms.ModelChoiceField(queryset = Ciudad.objects.none(), empty_label=None)
	modelo = forms.ModelChoiceField(queryset = Modelo.objects.none(), empty_label=None)
	marca = forms.ModelChoiceField(queryset = Marca.objects.all(), empty_label=None)
	usuario = forms.CharField(disabled=True)
	
	class Meta:
		#fields = ('anio','precio','esta_inspeccionado', 'provincia', 'ciudad', 'dueno')
		exclude = ('id','esta_inspeccionado','inspeccion',)
		model = Carro
		readonly_fields = ('usuario',)
	def __init__(self, *args, **kwargs):
		super(CarroForm, self).__init__(*args, **kwargs)
		self.fields['provincia'].empty_label = None
		
class ColorForm(ModelForm):
	exclude = ('id',)
class ModeloForm(ModelForm):
	exclude = ('id',)
class ProvinciaForm(ModelForm):
	exclude = ('id',)
class CiudadForm(ModelForm):
	exclude = ('id',)
class MarcaForm(forms.Form):
	marca = forms.ModelChoiceField(queryset = Marca.objects.all())
	modelo = forms.ModelChoiceField(queryset = Modelo.objects.all())
	
class SignUpForm(UserCreationForm):
	username = forms.CharField(  max_length=32, label='Username')
	first_name = forms.CharField(max_length=32, label='First name')
	last_name=forms.CharField( max_length=32, label='Last name')
	email=forms.EmailField(max_length=64, help_text='Enter a valid email address')
	cedula = forms.CharField(max_length=10, label='Cedula')
	celular = forms.CharField(max_length=10, label='Celular')
	ciudad = forms.CharField(max_length=10, label='Ciudad')
	password1=forms.CharField(max_length=30, label='Password')
	password2=forms.CharField(max_length=20, label='Password Again')
	
	class Meta(UserCreationForm.Meta):
		model = User
		fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email','celular','ciudad',)
		
